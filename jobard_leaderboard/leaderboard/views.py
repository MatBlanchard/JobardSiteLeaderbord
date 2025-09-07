from django.shortcuts import render
from admin_app.models import Campaign
from .models import LapTime
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery

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
        .order_by('lap_time_ms')
    )

    layouts = list(
        campaign.layouts.all().annotate(
            best_laptime_id=Subquery(best_lap_for_layout.values('id')[:1])
        )
    )

    best_ids = [l.best_laptime_id for l in layouts if l.best_laptime_id]
    best_laps_by_id = LapTime.objects.in_bulk(best_ids)

    for l in layouts:
        l.best_laptime = best_laps_by_id.get(l.best_laptime_id)

    return render(request, 'leaderboard/campaign_detail.html', {
        'campaign': campaign,
        'layouts': layouts
    })
