from django.urls import path
from . import views

urlpatterns = [
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("users/", views.manage_users, name="manage_users"),
    path("campaigns/", views.manage_campaigns, name="manage_campaigns"),
    path("campaigns/delete/<int:campaign_id>/", views.delete_campaign, name="delete_campaign"),
    path("campaigns/detail/<int:campaign_id>/", views.campaign_detail, name="campaign_detail"),
]
