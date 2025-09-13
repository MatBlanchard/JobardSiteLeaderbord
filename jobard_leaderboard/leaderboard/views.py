from django.shortcuts import render
from admin_app.models import Campaign
from .models import LapTime, Medal
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Count, Subquery, Q

def _fmt_ms(ms: int | None) -> str:
    if ms is None:
        return ""
    ms = int(ms)
    minutes, rem = divmod(ms, 60000)
    seconds, milli = divmod(rem, 1000)
    return f"{minutes}:{seconds:02d}.{milli:03d}"

@login_required
def dashboard(request):
    campaigns = Campaign.objects.all().prefetch_related('cars', 'layouts').order_by('name')
    return render(request, 'leaderboard/dashboard.html', {
        'campaigns': campaigns,
    })

@login_required
def campaign_detail(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)

    best_lap_for_layout = (
        LapTime.objects
        .filter(
            layout=OuterRef('pk'),
            car__in=campaign.cars.all(),
        )
        .order_by('lap_time_ms', 'pk')
    )

    driver_id = getattr(request.user, 'driver_id', None)
    best_user_lap_for_layout = (
        LapTime.objects
        .filter(
            layout=OuterRef('pk'),
            driver_id=driver_id,
            car__in=campaign.cars.all(),
        )
        .order_by('lap_time_ms', 'pk')
    )

    layouts = list(
        campaign.layouts.all().annotate(
            best_laptime_id=Subquery(best_lap_for_layout.values('id')[:1]),
            best_user_laptime_id = Subquery(best_user_lap_for_layout.values('id')[:1]),
            player_count = Count(
                'lap_times',
                filter=Q(lap_times__car__in=campaign.cars.all()),
                distinct=True
            )
        )
        .order_by('track__name', 'name')
    )

    ids = ({l.best_laptime_id for l in layouts if l.best_laptime_id}
           | {l.best_user_laptime_id for l in layouts if l.best_user_laptime_id})

    lap_map = LapTime.objects.only('id', 'lap_time_ms', 'car_id', 'driver_id').in_bulk(ids)

    medals = list(Medal.objects.order_by('coef'))

    for l in layouts:
        l.best_laptime = lap_map.get(l.best_laptime_id)  # WR
        l.best_user_laptime = lap_map.get(l.best_user_laptime_id)  # User

        l.best_medal = None
        l.next_medal = None
        l.next_medal_laptime = None

        if not l.best_laptime:
            continue

        wr_ms = l.best_laptime.lap_time_ms

        idx_best = None
        if l.best_user_laptime:
            user_ms = l.best_user_laptime.lap_time_ms
            ratio = user_ms / wr_ms
            for i, m in enumerate(medals):
                if ratio <= m.coef:
                    l.best_medal = m
                    idx_best = i
                    break

        if l.best_user_laptime is None:
            next_idx = len(medals) - 1 if medals else None
        else:
            if idx_best is None:
                next_idx = len(medals) - 1 if medals else None
            elif idx_best == 0:
                next_idx = None
            else:
                next_idx = idx_best - 1

        if next_idx is not None and 0 <= next_idx < len(medals):
            nm = medals[next_idx]
            l.next_medal = nm
            target_ms = wr_ms * nm.coef
            l.next_medal_laptime = _fmt_ms(target_ms)

    return render(request, 'leaderboard/campaign_detail.html', {
        'campaign': campaign,
        'layouts': layouts
    })
