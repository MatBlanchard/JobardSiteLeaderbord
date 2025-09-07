from django.shortcuts import render
from admin_app.models import Campaign
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    campaigns = Campaign.objects.all().prefetch_related('cars', 'layouts').order_by('name')
    return render(request, 'leaderboard/dashboard.html', {
        'campaigns': campaigns,
    })

@login_required
def campaign_detail(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    return render(request, 'leaderboard/campaign_detail.html', {
        'campaign': campaign,
    })
