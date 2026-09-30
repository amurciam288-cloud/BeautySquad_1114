const notice = document.querySelector("[data-notice]");

function showNotice(message, isError = false) {
  notice.textContent = message;
  notice.classList.toggle("error", isError);
}

async function api(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  const data = response.status === 204 ? null : await response.json();

  if (!response.ok) {
    throw new Error(data?.error || "No fue posible completar la operación.");
  }

  return data;
}

async function loadSession() {
  try {
    return (await api("/api/auth/me")).usuario;
  } catch {
    return null;
  }
}

function updateNavigation(user) {
  document.querySelector("[data-auth-link]").hidden = Boolean(user);
  document.querySelector("[data-logout]").hidden = !user;
  document.querySelector("[data-admin-link]").hidden = user?.role !== "admin";
}

async function populateBookings(user) {
  const services = await api("/api/services/");
  const slots = await api("/api/appointments/availability");
  const serviceSelect = document.querySelector("[data-services]");
  const slotSelect = document.querySelector("[data-slots]");

  serviceSelect.innerHTML = '<option value="">Selecciona un servicio</option>' + services.servicios
    .map((service) => `<option value="${service.id}">${service.name} — $${service.price}</option>`)
    .join("");
  slotSelect.innerHTML = '<option value="">Selecciona un horario</option>' + slots.horarios
    .map((slot) => `<option value="${slot.date}|${slot.time}">${slot.date} · ${slot.time}</option>`)
    .join("");

  if (!user) return;

  const appointments = await api("/api/appointments/");
  const section = document.querySelector("[data-my-appointments]");
  const list = document.querySelector("[data-appointments-list]");
  section.hidden = false;
  list.innerHTML = appointments.citas.length
    ? appointments.citas.map((appointment) => `<li>${appointment.date} · ${appointment.time} — ${appointment.status}</li>`).join("")
    : "<li>Aún no tienes citas.</li>";
}

async function renderAdminAppointments() {
  const response = await api("/api/appointments/");
  const container = document.querySelector("[data-admin-appointments]");
  container.innerHTML = response.citas.length
    ? `<table><thead><tr><th>Fecha</th><th>Cliente</th><th>Servicio</th><th>Estado</th><th>Acción</th></tr></thead><tbody>${response.citas.map((appointment) => `
      <tr>
        <td>${appointment.date} ${appointment.time}</td>
        <td>${appointment.user.name}</td>
        <td>${appointment.service.name}</td>
        <td>${appointment.status}</td>
        <td>${appointment.status === "pending" ? `<button data-status="confirmed" data-appointment="${appointment.id}">Confirmar</button> <button data-status="cancelled" data-appointment="${appointment.id}">Cancelar</button>` : "—"}</td>
      </tr>`).join("")}</tbody></table>`
    : "<p>No hay citas registradas.</p>";
}

function attachForms(user) {
  document.querySelectorAll("[data-auth-form]").forEach((form) => {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const payload = Object.fromEntries(new FormData(form));
      try {
        await api(`/api/auth/${form.dataset.mode === "login" ? "login" : "register"}`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
        window.location.href = form.dataset.mode === "login" ? "/bookings" : "/login";
      } catch (error) {
        showNotice(error.message, true);
      }
    });
  });

  const bookingForm = document.querySelector("[data-booking-form]");
  if (bookingForm) {
    bookingForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!user) {
        window.location.href = "/login";
        return;
      }
      const values = Object.fromEntries(new FormData(bookingForm));
      const [date, time] = values.slot.split("|");
      try {
        await api("/api/appointments/", {
          method: "POST",
          body: JSON.stringify({ date, time, service_id: Number(values.service_id) }),
        });
        showNotice("Tu cita fue reservada correctamente.");
        await populateBookings(user);
      } catch (error) {
        showNotice(error.message, true);
      }
    });
  }

  document.querySelector("[data-service-form]")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await api("/api/services/", { method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(event.currentTarget))) });
      event.currentTarget.reset();
      showNotice("Servicio guardado correctamente.");
    } catch (error) { showNotice(error.message, true); }
  });

  document.querySelector("[data-slot-form]")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await api("/api/appointments/availability", { method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(event.currentTarget))) });
      event.currentTarget.reset();
      showNotice("Horario publicado correctamente.");
    } catch (error) { showNotice(error.message, true); }
  });

  document.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-appointment]");
    if (!button) return;
    try {
      await api(`/api/appointments/${button.dataset.appointment}/status`, {
        method: "PATCH",
        body: JSON.stringify({ status: button.dataset.status }),
      });
      await renderAdminAppointments();
      showNotice("Estado de cita actualizado.");
    } catch (error) { showNotice(error.message, true); }
  });
}

async function start() {
  const user = await loadSession();
  updateNavigation(user);
  document.querySelector("[data-logout]").addEventListener("click", async () => {
    await api("/api/auth/logout", { method: "POST" });
    window.location.href = "/";
  });
  attachForms(user);

  if (document.body.dataset.page === "bookings") {
    await populateBookings(user);
  }

  if (document.body.dataset.page === "admin" && user?.role === "admin") {
    document.querySelector("[data-admin-panel]").hidden = false;
    document.querySelector("[data-admin-denied]").hidden = true;
    await renderAdminAppointments();
  }
}

start().catch((error) => showNotice(error.message, true));
