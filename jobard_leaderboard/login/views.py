from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import EmailLoginForm, SignUpForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect("leaderboard:dashboard")

    form = EmailLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(request.GET.get("next") or reverse("leaderboard:dashboard"))

    return render(request, "login/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login:login")

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("leaderboard:dashboard")

    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("leaderboard:dashboard")

    return render(request, "login/signup.html", {"form": form})
