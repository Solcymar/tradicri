from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente


class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefono = forms.CharField(max_length=20, required=False)
    direccion = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nombre', 'email', 'telefono', 'direccion']
