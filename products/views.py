from django.shortcuts import render
from .models import Producto

def home(request):
    return render(request, 'Home_nuevo.html')

def lista_productos(request):
    productos = Producto.objects.filter(activo=True)
    return render(request, 'Tienda.html', {'productos': productos})

def quienes_somos(request):
    return render(request, 'Quienes_somos.html')