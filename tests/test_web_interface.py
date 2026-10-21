from datetime import date, timedelta

from models import Availability, Service, TeamMember, db


def future_date():
    return (date.today() + timedelta(days=30)).isoformat()


def test_public_home_renders_services_page(client, app):
    with app.app_context():
        db.session.add(Service(name="Brows", description="Basic", price=20))
        db.session.commit()

    response = client.get("/")

    assert response.status_code == 200
    assert b"BeautySquad" in response.data
    assert b"Brows" in response.data


def test_shared_layout_renders_group_footer(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b'class="site-footer"' in response.data
    assert "Proyecto desarrollado por las integrantes del grupo: Cathalina Murcia, Valentina Alape y Liseth Reyes.".encode() in response.data


def test_public_home_renders_confirmed_project_members_without_fictitious_profiles(client, app):
    with app.app_context():
        db.session.add_all([
            TeamMember(name="Cathalina Murcia", specialty="Equipo BeautySquad", image_url="/static/placeholder-team.svg"),
            TeamMember(name="Valentina Alape", specialty="Equipo BeautySquad", image_url="/static/placeholder-team.svg"),
            TeamMember(name="Liseth Reyes", specialty="Equipo BeautySquad", image_url="/static/placeholder-team.svg"),
        ])
        db.session.commit()

    response = client.get("/")

    assert response.status_code == 200
    for name in ["Cathalina Murcia", "Valentina Alape", "Liseth Reyes"]:
        assert response.data.count(name.encode()) >= 2
    for fictitious_name in ["Laura Gómez", "Mariana Rojas", "Sofía Torres", "Camila Vargas"]:
        assert fictitious_name.encode() not in response.data
    assert b"integrantes reales del proyecto" in response.data
    assert b"datos de demostraci\xc3\xb3n del cat\xc3\xa1logo" in response.data


def test_navigation_marks_the_current_page_for_keyboard_and_screen_reader_users(client):
    cases = [
        ("/", b'href="/" aria-current="page"'),
        ("/bookings", b'href="/bookings" aria-current="page"'),
        ("/login", b'href="/login" data-auth-link aria-current="page"'),
        ("/register", b'href="/login" data-auth-link aria-current="page"'),
        ("/admin", b'href="/admin" data-admin-link aria-current="page"'),
    ]

    for path, current_link in cases:
        response = client.get(path)

        assert response.status_code == 200
        assert 'aria-label="Navegación principal"'.encode() in response.data
        assert current_link in response.data


def test_styles_include_visible_focus_and_non_color_navigation_states(client):
    response = client.get("/static/styles.css")

    assert response.status_code == 200
    assert b"a:focus-visible" in response.data
    assert b"button:focus-visible" in response.data
    assert b"input:focus-visible" in response.data
    assert b"select:focus-visible" in response.data
    assert b'nav a[aria-current="page"]' in response.data
    assert b"text-decoration: underline" in response.data


def test_admin_page_renders_visual_dashboard_sections_and_controls(client):
    response = client.get("/admin")

    assert response.status_code == 200
    for marker in [
        b'data-admin-summary',
        b'data-summary-pending',
        b'data-summary-confirmed',
        b'data-summary-services',
        b'data-summary-schedules',
        b'data-appointment-filters',
        b'name="status"',
        b'name="date"',
        b'data-admin-services',
        b'data-admin-schedules',
    ]:
        assert marker in response.data


def test_admin_dashboard_script_uses_existing_filters_and_status_actions(client):
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert b"/api/appointments/" in response.data
    assert b"new URLSearchParams" in response.data
    assert b'data-status="confirmed"' in response.data
    assert b'data-status="cancelled"' in response.data
    assert b"refreshAdminDashboard" in response.data


def test_public_api_exposes_only_available_slots(client, app):
    with app.app_context():
        db.session.add_all([
            Availability(date=future_date(), time="10:00", is_available=True),
            Availability(date=future_date(), time="11:00", is_available=False),
        ])
        db.session.commit()

    response = client.get("/api/appointments/availability")

    assert response.status_code == 200
    assert response.get_json()["horarios"] == [{
        "id": 1,
        "date": future_date(),
        "time": "10:00",
    }]


def test_bookings_page_exposes_local_empty_state_messages_and_retry_action(client):
    response = client.get("/bookings")

    assert response.status_code == 200
    assert b'data-booking-retry' in response.data
    assert b">Reintentar<" in response.data
    assert "No hay servicios publicados todavía.".encode() in response.data
    assert b"No hay horarios disponibles." in response.data


def test_bookings_page_exposes_booking_state_region_and_initial_loading_controls(client):
    response = client.get("/bookings")

    assert response.status_code == 200
    assert b'data-booking-status' in response.data
    assert b"Cargando servicios y horarios..." in response.data
    assert b'data-booking-submit disabled' in response.data
    assert b"Confirmar reserva" in response.data


def test_booking_state_messages_are_present_in_frontend_script(client):
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert b"Reservando cita..." in response.data
    assert b"Tu cita fue reservada correctamente." in response.data


def test_bookings_page_exposes_simulated_payment_form_without_card_fields(client):
    page = client.get("/bookings")
    script = client.get("/static/app.js")

    assert b"Pagar ahora" in script.data
    assert b"Tarjeta simulada" in page.data
    assert b"PSE simulado" in page.data
    assert b"Efectivo simulado" in page.data
    assert b"no hay cobros reales" in page.data
    assert b'name="card_number"' not in page.data
    assert b'name="cvv"' not in page.data


def test_bookings_page_exposes_client_appointment_status_and_cancel_flow(client):
    page = client.get("/bookings")
    script = client.get("/static/app.js")

    assert b"Consulta aqu\xc3\xad tus pr\xc3\xb3ximas citas" in page.data
    assert b"data-appointments-list" in page.data
    assert b"Pendiente" in script.data
    assert b"Cancelar cita" in script.data
    assert b"/api/appointments/${button.dataset.appointment}/cancel" in script.data
    assert b"window.confirm" in script.data


def test_logged_in_user_can_read_own_session_data(client):
    client.post(
        "/api/auth/register",
        json={"name": "Client", "email": "client@example.com", "password": "secure-password"},
    )
    client.post(
        "/api/auth/login",
        json={"email": "client@example.com", "password": "secure-password"},
    )

    response = client.get("/api/auth/me")

    assert response.status_code == 200
    assert response.get_json()["usuario"] == {
        "id": 1,
        "name": "Client",
        "email": "client@example.com",
        "role": "client",
    }
