let carrito = [];

function actualizarCarrito() {
    const modalBody = document.getElementById("contenidoCarrito");
    const badge = document.getElementById("contadorCarrito");
    modalBody.innerHTML = "";
    let total = 0;

    carrito.forEach((item, index) => {
        const subtotal = item.precio * item.cantidad;
        total += subtotal;
        modalBody.innerHTML += `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <div>
                    <strong>${item.nombre}</strong> (${item.tipo})<br>
                    Cantidad: ${item.cantidad} - Subtotal: S/ ${subtotal.toFixed(2)}
                </div>
                <button class="btn btn-sm btn-danger" onclick="eliminarItem(${index})">Eliminar</button>
            </div>
        `;
    });

    if (carrito.length === 0) {
        modalBody.innerHTML = "<p class='text-center'>Tu carrito está vacío.</p>";
    } else {
        modalBody.innerHTML += `<hr><h5 class="text-end">Total: S/ ${total.toFixed(2)}</h5>`;
    }

    badge.textContent = carrito.length;
}

function eliminarItem(index) {
    carrito.splice(index, 1);
    actualizarCarrito();
}

function agregarItemAlCarrito(id, tipo, nombre, precio) {
    const itemExistente = carrito.find(item => item.id === id && item.tipo === tipo);
    if (itemExistente) {
        itemExistente.cantidad += 1;
    } else {
        carrito.push({ id, tipo, nombre, precio, cantidad: 1 });
    }
    actualizarCarrito();
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".agregar-carrito").forEach(boton => {
        boton.addEventListener("click", () => {
            const id = parseInt(boton.dataset.id);
            const tipo = boton.dataset.tipo;
            const nombre = boton.dataset.nombre;
            const precio = parseFloat(boton.dataset.precio);
            agregarItemAlCarrito(id, tipo, nombre, precio);
        });
    });
});

function enviarPedido() {
    const fechaEvento = document.getElementById("fecha_evento").value;
    if (!fechaEvento) {
        alert("Por favor selecciona una fecha para el evento.");
        return;
    }

    const form = document.createElement("form");
    form.method = "POST";
    form.action = realizarPedidoURL; // Definido globalmente en plantilla

    const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

    form.innerHTML = `
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrf}">
        <input type="hidden" name="carrito_serializado" value='${JSON.stringify(carrito)}'>
        <input type="hidden" name="fecha_evento" value='${fechaEvento}'>
    `;

    document.body.appendChild(form);
    form.submit();
}
