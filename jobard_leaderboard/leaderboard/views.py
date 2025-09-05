from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Campaign, Car, Layout

User = get_user_model()

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

@login_required
@staff_required
def admin_dashboard(request):
    return render(request, "leaderboard/admin_dashboard.html")


@login_required
@staff_required
def manage_users(request):
    users = User.objects.all()
    return render(request, "leaderboard/manage_users.html", {
        "users": users,
        "active_tab": "users"
    })

@login_required
@staff_required
def manage_campaigns(request):
    campaigns = Campaign.objects.all().order_by("name")

    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Campaign.objects.create(name=name)
            return redirect("manage_campaigns")

    return render(request, "leaderboard/manage_campaigns.html", {
        "campaigns": campaigns,
        "active_tab": "campaigns"
    })


@login_required
@staff_required
def campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    cars = Car.objects.all().order_by("name")
    layouts = Layout.objects.select_related("track").all().order_by("track__name", "name")

    if request.method == "POST":
        selected_cars = request.POST.get("cars", "").split(",")
        selected_layouts = request.POST.get("layouts", "").split(",")

        campaign.cars.set([c for c in selected_cars if c])
        campaign.layouts.set([l for l in selected_layouts if l])
        campaign.save()
        return redirect("campaign_detail", campaign_id=campaign.id)

    return render(request, "leaderboard/campaign_detail.html", {
        "campaign": campaign,
        "cars": cars,
        "layouts": layouts
    })

@login_required
@staff_required
def delete_campaign(request, campaign_id):
    if request.method == "POST":
        campaign = get_object_or_404(Campaign, id=campaign_id)
        campaign.delete()
    return redirect("manage_campaigns")