from django.db import models
from django.conf import settings
from products.models import Producto

class Carrito(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.get_full_name()}"
    
    def total(self):
        return sum(item.subtotal() for item in self.items.all())
    
    def cantidad_items(self):
        return sum(item.cantidad for item in self.items.all())
    
    def vaciar(self):
        self.items.all().delete()

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto_nombre = models.CharField(max_length=100)  # Nombre congelado al momento de añadir
    tipo_empaque = models.CharField(max_length=50)       # Ej: "Copa", "Galón"
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Precio congelado
    cantidad = models.PositiveIntegerField(default=1)
    agregado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['carrito', 'producto_nombre', 'tipo_empaque']

    def __str__(self):
        return f"{self.cantidad} x {self.producto_nombre} ({self.tipo_empaque})"
    
    def subtotal(self):
        return self.precio_unitario * self.cantidad