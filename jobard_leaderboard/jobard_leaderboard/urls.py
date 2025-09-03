from django.contrib import admin
from django.urls import path, include
from login import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("login.urls", "login"), namespace="login")),
]
