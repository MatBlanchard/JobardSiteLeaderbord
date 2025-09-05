from django.urls import path
from . import views

urlpatterns = [
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("categories/", views.manage_categories, name="manage_categories"),
    path("users/", views.manage_users, name="manage_users"),
]
