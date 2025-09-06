from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import EmailLoginForm, SignUpForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect("login:dashboard")

    form = EmailLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(request.GET.get("next") or reverse("login:dashboard"))

    return render(request, "login/login.html", {"form": form})

@login_required
def dashboard(request):
    return render(request, "leaderboard/dashboard.html")

def logout_view(request):
    logout(request)
    return redirect("login:login")

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("login:dashboard")

    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("login:dashboard")

    return render(request, "login/signup.html", {"form": form})
