from datetime import date, timedelta

from models import Availability, Service, db


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
