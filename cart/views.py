from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import json
from .models import Carrito, ItemCarrito
from orders.models import Factura, DetalleFactura

def obtener_o_crear_carrito(request):
    if not request.user.is_authenticated:
        return None
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user, activo=True)
    return carrito


@login_required
@require_POST
def añadir_al_carrito(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Debes iniciar sesión'}, status=401)

    try:
        data = json.loads(request.body)
        carrito = obtener_o_crear_carrito(request)
        
        producto_nombre = data.get('nombre')
        tipo_empaque = data.get('tipo')
        precio = float(data.get('precio'))
        cantidad = int(data.get('cantidad', 1))
        
        item, creado = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto_nombre=producto_nombre,
            tipo_empaque=tipo_empaque,
            defaults={'precio_unitario': precio, 'cantidad': cantidad}
        )
        
        if not creado:
            item.cantidad += cantidad
            item.save()
            
        return JsonResponse({
            'success': True, 
            'total_items': carrito.cantidad_items()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@login_required
def ver_carrito(request):
    carrito = obtener_o_crear_carrito(request)
    
    if carrito:
        items = carrito.items.all()
        total = carrito.total()
    else:
        items = []
        total = 0
    
    context = {
        'carrito': carrito,
        'items': items,
        'total': total,
        'carrito_items': list(items.values(
            'id', 'producto_nombre', 'tipo_empaque', 'precio_unitario', 'cantidad'
        ))
    }
    
    return render(request, 'carrito.html', context)

@login_required
@require_POST
def finalizar_compra(request):
    """Crear factura y vaciar carrito"""
    print(f"🔔 FINALIZAR COMPRA - Usuario: {request.user}")
    
    try:
        carrito = get_object_or_404(Carrito, usuario=request.user, activo=True)
        print(f"🛒 Carrito encontrado: {carrito.id}")
        print(f"📦 Items en carrito: {carrito.items.count()}")
        
        if not carrito.items.exists():
            print("⚠️ Carrito vacío")
            messages.warning(request, 'Tu carrito está vacío.')
            return redirect('ver_carrito')
        
        # Crear factura
        total = carrito.total()
        print(f"💰 Total: {total}")
        
        factura = Factura.objects.create(
            usuario=request.user,
            nombres_cliente=request.user.nombres,
            apellidos_cliente=request.user.apellidos,
            total=total
        )
        print(f"🧾 Factura creada: #{factura.id}")
        
        # Crear detalles
        for item in carrito.items.all():
            DetalleFactura.objects.create(
                factura=factura,
                producto_nombre=item.producto_nombre,
                tipo_empaque=item.tipo_empaque,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                subtotal=item.subtotal()
            )
            print(f"  - Detalle: {item.producto_nombre} x{item.cantidad}")
        
        # Vaciar carrito
        carrito.vaciar()
        print("✅ Carrito vaciado")
        
        messages.success(request, f'¡Compra exitosa! Factura #{factura.id} creada.')
        return redirect('detalle_factura', factura_id=factura.id)
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        messages.error(request, f'Error al procesar la compra: {str(e)}')
        return redirect('ver_carrito')

@login_required
def detalle_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id, usuario=request.user)
    return render(request, 'factura_detalle.html', {'factura': factura})

@login_required
def vaciar_carrito(request):
    """Vaciar el carrito del usuario"""
    carrito = obtener_o_crear_carrito(request)
    if carrito:
        carrito.vaciar()
    return redirect('ver_carrito')