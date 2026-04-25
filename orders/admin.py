from django.contrib import admin
from .models import Factura, DetalleFactura

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'nombres_cliente', 'fecha', 'total', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('nombres_cliente', 'apellidos_cliente')

@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'producto_nombre', 'tipo_empaque', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('producto_nombre', 'tipo_empaque')
    list_filter = ('tipo_empaque',)