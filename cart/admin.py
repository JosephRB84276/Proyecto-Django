from django.contrib import admin
from .models import Carrito, ItemCarrito

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'activo', 'creado_en', 'total')
    list_filter = ('activo', 'creado_en')
    
    def total(self, obj):
        return f"${obj.total():,.0f}"
    total.short_description = 'Total'

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto_nombre', 'tipo_empaque', 'precio_unitario', 'cantidad', 'subtotal')
    list_filter = ('tipo_empaque', 'agregado_en')
    search_fields = ('producto_nombre',)
    
    def subtotal(self, obj):
        return f"${obj.subtotal():,.0f}"
    subtotal.short_description = 'Subtotal'