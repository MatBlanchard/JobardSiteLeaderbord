from django import forms
from .models import Category, Car, Class

class CategoryForm(forms.ModelForm):
    cars = forms.ModelMultipleChoiceField(
        queryset=Car.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Category
        fields = ["name", "cars"]


class ClassSelectionForm(forms.Form):
    car_class = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        required=False,
        label="Ajouter toutes les voitures d’une classe"
    )