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
