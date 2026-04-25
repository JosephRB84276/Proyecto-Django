from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'tipo_empaque', 'precio', 'stock', 'activo')
    search_fields = ('nombre_producto', 'descripcion')
    list_filter = ('tipo_empaque', 'activo')