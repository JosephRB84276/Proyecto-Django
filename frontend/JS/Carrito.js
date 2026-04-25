// carrito.js 

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


document.addEventListener('click', function(e) {
    const boton = e.target.closest('.btn-secundary');
    if (!boton) return;

    e.preventDefault();
    e.stopPropagation();

    const card = boton.closest('.producto-card');
    const nombre = boton.dataset.nombre;
    const select = card.querySelector('.form-select');
    const cantidadInput = card.querySelector('.cantidad');

    if (!select || !cantidadInput) return;

    const tipo = select.options[select.selectedIndex].text.split(' - ')[0];
    const precio = parseInt(select.value);
    const cantidad = parseInt(cantidadInput.value);

    if (cantidad <= 0 || isNaN(cantidad)) {
        alert("La cantidad debe ser mayor a 0");
        return;
    }

    // Petición AJAX al backend
    fetch('/carrito/añadir/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ nombre, tipo, precio, cantidad })
    })
    .then(response => {
        if (response.status === 401) {
            alert("Debes iniciar sesión para añadir productos al carrito.");
            window.location.href = '/usuarios/login/';
            throw new Error('No autenticado');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Actualizar contador del navbar
            const contador = document.getElementById('contador-carrito');
            if (contador) {
                contador.textContent = `(${data.total_items})`;
            }
            alert(`✅ ${nombre} (${tipo}) añadido al carrito`);
        } else {
            alert('❌ Error: ' + (data.error || 'No se pudo añadir el producto'));
        }
    })
    .catch(error => {
        console.error('Error al añadir al carrito:', error);
        alert('Ocurrió un error al procesar la solicitud. Intenta nuevamente.');
    });
});


function vaciarCarrito() {
    if (confirm('¿Estás seguro de vaciar el carrito?')) {
        window.location.href = '/carrito/vaciar/';
    }
}