from django.urls import path
from . import views

app_name = "leaderboard"

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('campaign/<int:campaign_id>/', views.campaign_detail, name='campaign_detail'),
]