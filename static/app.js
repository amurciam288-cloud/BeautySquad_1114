const notice = document.querySelector("[data-notice]");
const BOOKING_LOAD_ERROR = "No se pudieron cargar los datos. Verifica que el servidor esté funcionando.";
const EMPTY_SERVICES = "No hay servicios publicados todavía.";
const EMPTY_SLOTS = "No hay horarios disponibles.";
const BOOKING_LOADING = "Cargando servicios y horarios...";
const BOOKING_SUBMITTING = "Reservando cita...";
const BOOKING_SUCCESS = "Tu cita fue reservada correctamente.";
const STATUS_LABELS = {
  pending: "Pendiente",
  confirmed: "Confirmada",
  cancelled: "Cancelada",
  completed: "Completada",
};
const PAYMENT_METHOD_LABELS = {
  tarjeta_simulada: "Tarjeta simulada",
  pse_simulado: "PSE simulado",
  efectivo_simulado: "Efectivo simulado",
};

function showNotice(message, isError = false) {
  notice.textContent = message;
  notice.classList.toggle("error", isError);
}

function showBookingStatus(message, isError = false) {
  const status = document.querySelector("[data-booking-status]");
  if (!status) return;
  status.textContent = message;
  status.classList.toggle("error", isError);
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
  const serviceSelect = document.querySelector("[data-services]");
  const slotSelect = document.querySelector("[data-slots]");
  const retryButton = document.querySelector("[data-booking-retry]");
  const bookingSubmit = document.querySelector("[data-booking-submit]");

  retryButton.hidden = true;
  serviceSelect.disabled = true;
  slotSelect.disabled = true;
  bookingSubmit.disabled = true;
  bookingSubmit.textContent = "Confirmar reserva";
  showBookingStatus(BOOKING_LOADING);

  try {
    const [services, slots] = await Promise.all([
      api("/api/services/"),
      api("/api/appointments/availability"),
    ]);
    const availableServices = services.servicios || [];
    const availableSlots = slots.horarios || [];

    serviceSelect.innerHTML = availableServices.length
      ? '<option value="">Selecciona un servicio</option>' + availableServices
        .map((service) => `<option value="${service.id}">${service.name} — $${service.price}</option>`)
        .join("")
      : `<option value="">${serviceSelect.dataset.emptyMessage || EMPTY_SERVICES}</option>`;
    slotSelect.innerHTML = availableSlots.length
      ? '<option value="">Selecciona un horario</option>' + availableSlots
        .map((slot) => `<option value="${slot.date}|${slot.time}">${slot.date} · ${slot.time}</option>`)
        .join("")
      : `<option value="">${slotSelect.dataset.emptyMessage || EMPTY_SLOTS}</option>`;
    serviceSelect.disabled = !availableServices.length;
    slotSelect.disabled = !availableSlots.length;
    bookingSubmit.disabled = !availableServices.length || !availableSlots.length;
    showBookingStatus(availableServices.length && availableSlots.length
      ? "Selecciona un servicio y un horario para continuar."
      : "No hay opciones disponibles para reservar.");
  } catch {
    serviceSelect.innerHTML = `<option value="">${BOOKING_LOAD_ERROR}</option>`;
    slotSelect.innerHTML = `<option value="">${BOOKING_LOAD_ERROR}</option>`;
    serviceSelect.disabled = true;
    slotSelect.disabled = true;
    retryButton.hidden = false;
    showBookingStatus(BOOKING_LOAD_ERROR, true);
    showNotice(BOOKING_LOAD_ERROR, true);
    return;
  }

  if (!user) return;

  const appointments = await api("/api/appointments/");
  const section = document.querySelector("[data-my-appointments]");
  const list = document.querySelector("[data-appointments-list]");
  section.hidden = false;
  list.innerHTML = appointments.citas.length
    ? appointments.citas.map((appointment) => `<li class="appointment-item"><div><strong>${escapeHtml(appointment.service.name)}</strong><span>$${escapeHtml(appointment.service.price)}</span><span>${escapeHtml(appointment.date)} · ${escapeHtml(appointment.time)}</span><span class="status status-${escapeHtml(appointment.status)}">${STATUS_LABELS[appointment.status] || escapeHtml(appointment.status)}</span>${appointment.payment ? ` <span class="status status-paid">Pago: ${escapeHtml(PAYMENT_METHOD_LABELS[appointment.payment.method] || "Simulado")}</span>` : appointment.status === "pending" ? ` <button type="button" data-client-pay data-appointment="${appointment.id}">Pagar ahora</button>` : ""}</div>${["pending", "confirmed"].includes(appointment.status) ? ` <button class="appointment-cancel" type="button" data-client-cancel data-appointment="${appointment.id}" aria-label="Cancelar cita de ${escapeHtml(appointment.service.name)} del ${escapeHtml(appointment.date)}">Cancelar cita</button>` : ""}</li>`).join("")
    : "<li>Aún no tienes citas.</li>";
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;",
  }[character]));
}

async function renderAdminSummary() {
  const [appointments, services, schedules] = await Promise.all([
    api("/api/appointments/"),
    api("/api/services/"),
    api("/api/appointments/availability"),
  ]);
  const counts = appointments.citas.reduce((result, appointment) => {
    result[appointment.status] = (result[appointment.status] || 0) + 1;
    return result;
  }, {});
  document.querySelector("[data-summary-pending]").textContent = counts.pending || 0;
  document.querySelector("[data-summary-confirmed]").textContent = counts.confirmed || 0;
  document.querySelector("[data-summary-services]").textContent = services.servicios.length;
  document.querySelector("[data-summary-schedules]").textContent = schedules.horarios.length;

  document.querySelector("[data-admin-services]").innerHTML = services.servicios.length
    ? `<ul class="resource-list">${services.servicios.map((service) => `<li><strong>${escapeHtml(service.name)}</strong><span>$${escapeHtml(service.price)}</span></li>`).join("")}</ul>`
    : '<p class="muted">No hay servicios publicados todavía.</p>';
  document.querySelector("[data-admin-schedules]").innerHTML = schedules.horarios.length
    ? `<ul class="resource-list">${schedules.horarios.slice(0, 5).map((slot) => `<li><strong>${escapeHtml(slot.date)}</strong><span>${escapeHtml(slot.time)}</span></li>`).join("")}</ul>${schedules.horarios.length > 5 ? `<p class="muted">+${schedules.horarios.length - 5} horarios más</p>` : ""}`
    : '<p class="muted">No hay horarios disponibles.</p>';
}

async function renderAdminAppointments(filters = {}) {
  const params = new URLSearchParams();
  if (filters.status) params.set("status", filters.status);
  if (filters.date) params.set("date", filters.date);
  const response = await api(`/api/appointments/${params.toString() ? `?${params}` : ""}`);
  const container = document.querySelector("[data-admin-appointments]");
  document.querySelector("[data-appointment-count]").textContent = `${response.citas.length} ${response.citas.length === 1 ? "cita" : "citas"}`;
  container.innerHTML = response.citas.length
     ? `<div class="table-scroll"><table><thead><tr><th>Fecha</th><th>Cliente</th><th>Servicio</th><th>Estado</th><th>Pago</th><th>Acción</th></tr></thead><tbody>${response.citas.map((appointment) => `
       <tr>
       <td><strong>${escapeHtml(appointment.date)}</strong><small>${escapeHtml(appointment.time)}</small></td>
       <td>${escapeHtml(appointment.user.name)}<small>${escapeHtml(appointment.user.email)}</small></td>
       <td>${escapeHtml(appointment.service.name)}</td>
       <td><span class="status status-${escapeHtml(appointment.status)}">${STATUS_LABELS[appointment.status] || escapeHtml(appointment.status)}</span></td>
       <td>${appointment.payment ? `<span class="status status-paid">${escapeHtml(PAYMENT_METHOD_LABELS[appointment.payment.method] || "Simulado")}</span><small>${escapeHtml(appointment.payment.reference)}</small>` : "Sin pago"}</td>
       <td class="actions">${appointment.status === "pending" ? `<button class="action-confirm" data-status="confirmed" data-appointment="${appointment.id}">Confirmar</button> <button class="action-cancel" data-status="cancelled" data-appointment="${appointment.id}">Cancelar</button>` : appointment.status === "confirmed" ? `<button class="action-cancel" data-status="cancelled" data-appointment="${appointment.id}">Cancelar</button>` : "—"}</td>
      </tr>`).join("")}</tbody></table></div>`
    : "<p>No hay citas registradas.</p>";
}

async function refreshAdminDashboard(filters = {}) {
  await Promise.all([renderAdminSummary(), renderAdminAppointments(filters)]);
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
  const retryButton = document.querySelector("[data-booking-retry]");
  retryButton?.addEventListener("click", () => populateBookings(user));
  if (bookingForm) {
    bookingForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!user) {
        window.location.href = "/login";
        return;
      }
      const values = Object.fromEntries(new FormData(bookingForm));
      const [date, time] = values.slot.split("|");
      const bookingSubmit = bookingForm.querySelector("[data-booking-submit]");
      const controls = bookingForm.querySelectorAll("select, button");
      controls.forEach((control) => { control.disabled = true; });
      bookingSubmit.textContent = BOOKING_SUBMITTING;
      showBookingStatus(BOOKING_SUBMITTING);
      try {
        await api("/api/appointments/", {
          method: "POST",
          body: JSON.stringify({ date, time, service_id: Number(values.service_id) }),
        });
        showNotice(BOOKING_SUCCESS);
        await populateBookings(user);
        showBookingStatus(BOOKING_SUCCESS);
      } catch (error) {
        showBookingStatus(error.message, true);
        showNotice(error.message, true);
        controls.forEach((control) => { control.disabled = false; });
        bookingSubmit.textContent = "Confirmar reserva";
      }
    });
  }

  document.querySelector("[data-payment-form]")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const appointmentId = form.dataset.appointment;
    const submit = form.querySelector("[data-payment-submit]");
    submit.disabled = true;
    try {
      const result = await api(`/api/appointments/${appointmentId}/payment`, {
        method: "POST",
        body: JSON.stringify({ method: new FormData(form).get("method") }),
      });
      showNotice(`Pago simulado registrado. Referencia: ${result.pago.reference}`);
      form.reset();
      document.querySelector("[data-payment-panel]").hidden = true;
      await populateBookings(user);
    } catch (error) {
      showNotice(error.message, true);
    } finally {
      submit.disabled = false;
    }
  });

  document.querySelector("[data-payment-cancel]")?.addEventListener("click", () => {
    document.querySelector("[data-payment-panel]").hidden = true;
  });

  document.querySelector("[data-service-form]")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await api("/api/services/", { method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(event.currentTarget))) });
      event.currentTarget.reset();
      showNotice("Servicio guardado correctamente.");
      await refreshAdminDashboard();
    } catch (error) { showNotice(error.message, true); }
  });

  document.querySelector("[data-slot-form]")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await api("/api/appointments/availability", { method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(event.currentTarget))) });
      event.currentTarget.reset();
      showNotice("Horario publicado correctamente.");
      await refreshAdminDashboard();
    } catch (error) { showNotice(error.message, true); }
  });

  document.addEventListener("click", async (event) => {
    const payButton = event.target.closest("[data-client-pay]");
    if (payButton) {
      const appointment = (await api("/api/appointments/")).citas.find((item) => item.id === Number(payButton.dataset.appointment));
      if (!appointment) return;
      const panel = document.querySelector("[data-payment-panel]");
      panel.hidden = false;
      panel.querySelector("[data-payment-appointment]").textContent = `${appointment.service.name} · ${appointment.date} · ${appointment.time}`;
      panel.querySelector("[data-payment-form]").dataset.appointment = appointment.id;
      panel.querySelector("[data-payment-form] select").focus();
      return;
    }
    const button = event.target.closest("[data-appointment][data-status]");
    if (!button) return;
    try {
      await api(`/api/appointments/${button.dataset.appointment}/status`, {
        method: "PATCH",
        body: JSON.stringify({ status: button.dataset.status }),
      });
       await refreshAdminDashboard(document.querySelector("[data-appointment-filters]") && Object.fromEntries(new FormData(document.querySelector("[data-appointment-filters]"))));
      showNotice("Estado de cita actualizado.");
    } catch (error) { showNotice(error.message, true); }
  });

  document.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-client-cancel]");
    if (!button) return;
    if (!window.confirm("¿Quieres cancelar esta cita?")) return;

    try {
      await api(`/api/appointments/${button.dataset.appointment}/cancel`, {
        method: "POST",
        body: JSON.stringify({ status: "cancelled" }),
      });
      showNotice("Cita cancelada correctamente.");
      await populateBookings(user);
    } catch (error) { showNotice(error.message, true); }
  });

  document.querySelector("[data-appointment-filters]")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    try { await renderAdminAppointments(Object.fromEntries(new FormData(event.currentTarget))); }
    catch (error) { showNotice(error.message, true); }
  });
  document.querySelector("[data-clear-filters]")?.addEventListener("click", async () => {
    const filters = document.querySelector("[data-appointment-filters]");
    filters.reset();
    try { await renderAdminAppointments(); }
    catch (error) { showNotice(error.message, true); }
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
    await refreshAdminDashboard();
  }
}

start().catch((error) => showNotice(error.message, true));
