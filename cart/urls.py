from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_carrito, name='ver_carrito'),
    path('añadir/', views.añadir_al_carrito, name='añadir_al_carrito'),
    path('vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('factura/<int:factura_id>/', views.detalle_factura, name='detalle_factura'),
]