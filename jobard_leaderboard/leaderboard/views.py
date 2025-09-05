from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Category, Car, Class
from .forms import CategoryForm, ClassSelectionForm

User = get_user_model()

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

@login_required
@staff_required
def admin_dashboard(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, "leaderboard/admin_dashboard.html", {"users": users})


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
def manage_categories(request):
    classes = Class.objects.prefetch_related("cars").all()
    return render(request, "leaderboard/manage_categories.html", {
        "classes": classes,
        "active_tab": "categories"
    })

@login_required
@staff_required
def manage_categories(request):
    if request.method == "POST":
        category_name = request.POST.get("category_name")
        selected_classes = request.POST.getlist("classes")
        selected_cars = request.POST.getlist("cars")

        if category_name:
            category = Category.objects.create(name=category_name)

            # Ajouter toutes les voitures des classes cochées
            if selected_classes:
                cars_from_classes = Car.objects.filter(class_ref_id__in=selected_classes)
                category.cars.add(*cars_from_classes)

            # Ajouter les voitures sélectionnées individuellement
            if selected_cars:
                cars = Car.objects.filter(id__in=selected_cars)
                category.cars.add(*cars)

            messages.success(request, f"Catégorie '{category_name}' créée ✅")
            return redirect("manage_categories")

    classes = Class.objects.prefetch_related("cars").all()
    categories = Category.objects.all()

    return render(request, "leaderboard/manage_categories.html", {
        "classes": classes,
        "categories": categories,
    })