from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Cliente
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def inicio(request):
    return render(request, 'inicio.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm()
        })

    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()  # guarda el usuario
                Cliente.objects.create(
                    nombre=form.cleaned_data['nombre'],
                    email=form.cleaned_data['email'],
                    telefono=form.cleaned_data['telefono'],
                    direccion=form.cleaned_data['direccion'],
                    fecha_registro=timezone.now(),
                )
                login(request, user)
                return redirect('inicio')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': form,
                    "error": 'El nombre de usuario o correo ya existe'
                })
        else:
            return render(request, 'signup.html', {
                'form': form,
                "error": 'Las contraseñas no coinciden o los datos no son válidos'
            })








def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('inicio')  # 👈 Redirige a la vista 'inicio'






@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')









def nosotros(request):
    return render(request, 'nosotros.html')

def carta(request):
    return render(request, 'carta.html')

def servicios(request):
    return render(request, 'servicios.html')

def quienes_somos(request):
    return render(request, 'quienes_somos.html')

def faq(request):
    return render(request, 'faq.html')

def productos(request):
    return render(request, 'productos.html')

def platos_especiales(request):
    return render(request, 'platos_especiales.html')

def combos(request):
    return render(request, 'combos.html')

