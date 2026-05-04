# config/context_processors.py
def navbar_context(request):
    return {
        'user_authenticated': request.user.is_authenticated,
        'user_name': request.user.nombres if request.user.is_authenticated else '',
    }

from cart.models import Carrito

def navbar_context(request):
    # Por defecto el carrito está en 0
    context = {'cart_count': 0}
    
    # Solo calculamos si el usuario ha iniciado sesión
    if request.user.is_authenticated:
        try:
            # Buscamos el carrito activo del usuario
            carrito = Carrito.objects.get(usuario=request.user, activo=True)
            # Contamos cuántos ítems hay dentro
            context['cart_count'] = carrito.items.count()
        except Carrito.DoesNotExist:
            pass # Si no tiene carrito, se queda en 0
            
    return context