from django.db import models
from django.conf import settings

class Factura(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombres_cliente = models.CharField(max_length=50)
    apellidos_cliente = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='completada', choices=[
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ])

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha']

    def __str__(self):
        return f"Factura #{self.id} - {self.nombres_cliente} {self.apellidos_cliente}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name='detalles', on_delete=models.CASCADE)
    producto_nombre = models.CharField(max_length=100)  # ← CAMPO DE TEXTO (no ForeignKey)
    tipo_empaque = models.CharField(max_length=50)       # ← CAMPO DE TEXTO
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalles de Factura'

    def __str__(self):
        return f"{self.cantidad} x {self.producto_nombre} ({self.tipo_empaque})"