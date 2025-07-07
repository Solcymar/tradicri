from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('carta/', views.carta, name='carta'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('faq/', views.faq, name='faq'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('mis_pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('confirmar_pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('ver_carrito_ajax/', views.ver_carrito_ajax, name='ver_carrito_ajax'),
    path('quitar-del-carrito/', views.quitar_del_carrito, name='quitar_del_carrito'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)