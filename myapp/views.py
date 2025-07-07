from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import (
    Cliente, PlatoEspecial, Combo, ComboPlato, PedidoCombo,
    PedidoPlato, PedidoDecoracion, Pedido, PedidoEstado, Decoracion
)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import datetime
from django.views.decorators.http import require_GET
from django.http import JsonResponse, HttpResponseBadRequest
import json

from .forms import CustomUserCreationForm
from .models import (
    Cliente, PlatoEspecial, Combo, ComboPlato, PedidoCombo,
    PedidoPlato, PedidoDecoracion, Pedido, PedidoEstado, Decoracion
)

import json
from datetime import datetime
def inicio(request):
    return render(request, 'inicio.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': CustomUserCreationForm()})

    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        try:
            user = form.save()
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
                'error': 'El nombre de usuario o correo ya existe'
            })
    else:
        return render(request, 'signup.html', {
            'form': form,
            'error': 'Las contraseñas no coinciden o los datos no son válidos'
        })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm()})

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
    login(request, user)
    return redirect('inicio')

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')

def nosotros(request):
    return render(request, 'nosotros.html')


def carta(request):
    platos_especiales = PlatoEspecial.objects.all()
    combos = Combo.objects.all()
    decoraciones = Decoracion.objects.all()
    return render(request, 'carta.html', {
        'platos_especiales': platos_especiales,
        'combos': combos,
        'decoraciones': decoraciones
    })



def quienes_somos(request):
    return render(request, 'quienes_somos.html')

def faq(request):
    return render(request, 'faq.html')


@require_POST
@login_required
def agregar_al_carrito(request):
    tipo = request.POST.get('tipo')
    item_id = request.POST.get('id')
    cantidad = int(request.POST.get('cantidad', 1))

    cliente, _ = Cliente.objects.get_or_create(
        email=request.user.email,
        defaults={'nombre': request.user.username}
    )

    pedido, _ = Pedido.objects.get_or_create(
        cliente=cliente,
        estado=PedidoEstado.PENDIENTE,
        defaults={'fecha_evento': timezone.now().date()}
    )

    if tipo == 'combo':
        try:
            combo = Combo.objects.get(pk=item_id)
            PedidoCombo.objects.create(
                pedido=pedido,
                combo=combo,
                cantidad=cantidad,
                precio_unitario=combo.precio
            )
        except Combo.DoesNotExist:
            return JsonResponse({'error': 'Combo no existe'}, status=400)

    elif tipo == 'plato':
        try:
            plato = PlatoEspecial.objects.get(pk=item_id)
            PedidoPlato.objects.create(
                pedido=pedido,
                plato=plato,
                cantidad=cantidad,
                precio_unitario=plato.precio
            )
        except PlatoEspecial.DoesNotExist:
            return JsonResponse({'error': 'Plato no existe'}, status=400)

    elif tipo == 'decoracion':
        try:
            decoracion = Decoracion.objects.get(pk=item_id)
            PedidoDecoracion.objects.create(
                pedido=pedido,
                decoracion=decoracion,
                cantidad=cantidad,
                precio_unitario=decoracion.precio_alquiler
            )
        except Decoracion.DoesNotExist:
            return JsonResponse({'error': 'Decoracion no existe'}, status=400)

    return JsonResponse({'success': True})




def confirmar_pedido(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'not_authenticated'})
    
    cliente = Cliente.objects.get(email=request.user.email)
    try:
        pedido = Pedido.objects.get(cliente=cliente, estado=PedidoEstado.PENDIENTE)
        pedido.estado = PedidoEstado.CONFIRMADO
        pedido.save()
        return JsonResponse({'success': True})
    except Pedido.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No hay pedido pendiente'})




@login_required
def mis_pedidos(request):
    cliente = Cliente.objects.get(email=request.user.email)
    pedidos = Pedido.objects.filter(cliente=cliente).order_by('-fecha_pedido')

    pedidos_con_items = []
    for pedido in pedidos:
        platos = PedidoPlato.objects.filter(pedido=pedido)
        combos = PedidoCombo.objects.filter(pedido=pedido)
        decoraciones = PedidoDecoracion.objects.filter(pedido=pedido)

        total = sum(p.precio_unitario * p.cantidad for p in platos) \
              + sum(c.precio_unitario * c.cantidad for c in combos) \
              + sum(d.precio_unitario * d.cantidad for d in decoraciones)

        pedidos_con_items.append({
            'pedido': pedido,
            'platos': platos,
            'combos': combos,
            'decoraciones': decoraciones,
            'total': total
        })

    return render(request, 'mis_pedidos.html', {'pedidos_con_items': pedidos_con_items})



@require_GET
@login_required
def ver_carrito_ajax(request):
    cliente = Cliente.objects.filter(email=request.user.email).first()
    pedido = Pedido.objects.filter(cliente=cliente, estado=PedidoEstado.PENDIENTE).first()

    pedidos = []
    if pedido:
        pedidos += [
            {
                'tipo': 'plato',
                'nombre': pp.plato.nombre,
                'cantidad': pp.cantidad,
                'precio_unitario': float(pp.precio_unitario),
            } for pp in pedido.pedidoplato_set.all()
        ]
        pedidos += [
            {
                'tipo': 'combo',
                'nombre': pc.combo.nombre,
                'cantidad': pc.cantidad,
                'precio_unitario': float(pc.precio_unitario),
            } for pc in pedido.pedidocombo_set.all()
        ]
        pedidos += [
            {
                'tipo': 'decoracion',
                'nombre': pd.decoracion.nombre,
                'cantidad': pd.cantidad,
                'precio_unitario': float(pd.precio_unitario),
            } for pd in pedido.pedidodecoracion_set.all()
        ]

    return JsonResponse({'pedidos': pedidos})


@require_POST
@login_required
def quitar_del_carrito(request):
    tipo = request.POST.get('tipo')
    nombre = request.POST.get('nombre')

    cliente = Cliente.objects.filter(email=request.user.email).first()
    pedido = Pedido.objects.filter(cliente=cliente, estado=PedidoEstado.PENDIENTE).first()

    if not pedido:
        return JsonResponse({'success': False, 'error': 'No hay pedido'})

    try:
        if tipo == 'plato':
            item = pedido.pedidoplato_set.get(plato__nombre=nombre)
        elif tipo == 'combo':
            item = pedido.pedidocombo_set.get(combo__nombre=nombre)
        elif tipo == 'decoracion':
            item = pedido.pedidodecoracion_set.get(decoracion__nombre=nombre)
        else:
            return JsonResponse({'success': False, 'error': 'Tipo inválido'})

        item.delete()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False, 'error': 'No se pudo eliminar'})
