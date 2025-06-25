"""
URL configuration for tracri project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py unico dentro del proyecto (por ejemplo, tradicri/urls.py)

from django.contrib import admin
from django.urls import path, include
from myapp import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('carta/', views.carta, name='carta'),
    path('servicios/', views.servicios, name='servicios'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('faq/', views.faq, name='faq'),
    path('productos/', views.productos, name='productos'),
    path('platos-especiales/', views.platos_especiales, name='platos_especiales'),
    path('combos/', views.combos, name='combos'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup')


]

