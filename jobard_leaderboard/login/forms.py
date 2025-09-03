from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "autofocus": True,
            "placeholder": "Adresse email",
            "class": "form-control"
        })
    )

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom d’utilisateur"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Adresse email"}),
        }
