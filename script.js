const formulario = document.getElementById("formularioCita");
const listaCitas = document.getElementById("listaCitas");
document.getElementById("fecha").min = new 
Date().toISOString().split("T")[0];

let citas = 
JSON.parse(localStorage.getItem("citas")) || [];

formulario.addEventListener("submit", function(evento) {

    evento.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const servicio = document.getElementById("servicio").value;
    const fecha = document.getElementById("fecha").value;
    const hora = document.getElementById("hora").value;

    const citaExiste = citas.some(function(cita) {
       return cita.fecha === fecha && cita.hora === 
    hora && cita.estado !== "Cancelada";
});

if (citaExiste) {
    alert("Ese horario ya está ocupado. Por favor selecciona otro.");
    return;
}

    const cita = {
        nombre: nombre,
        servicio: servicio,
        fecha: fecha,
        hora: hora,
        estado: "Confirmada"
    };

    citas.push(cita);

    localStorage.setItem("citas",
    JSON.stringify(citas));

    mostrarCitas();

    alert("¡Tu cita fue reservada correctamente!");
});


function mostrarCitas() {

    listaCitas.innerHTML = "";

    if (citas.length === 0) {
        listaCitas.innerHTML = "<p>No tienes citas registradas.</p>";
        return;
    }

    citas.forEach(function(cita, indice) {

        const div = document.createElement("div");

        div.classList.add("cita");

        div.innerHTML = `
            <p><strong>Nombre:</strong> ${cita.nombre}</p>
            <p><strong>Servicio:</strong> ${cita.servicio}</p>
            <p><strong>Fecha:</strong> ${cita.fecha}</p>
            <p><strong>Hora:</strong> ${cita.hora}</p>
            <p class="estado"><strong>Estado:</strong> ${cita.estado}</p>

            <button onclick="cancelarCita(${indice})">
                Cancelar cita
            </button>
        `;

        listaCitas.appendChild(div);
    });
}


function cancelarCita(indice) {

    citas[indice].estado = "Cancelada";

    localStorage.setItem("citas",
    JSON.stringify(citas));

    mostrarCitas();
}