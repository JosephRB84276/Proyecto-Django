from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tienda/', views.lista_productos, name='tienda'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
]