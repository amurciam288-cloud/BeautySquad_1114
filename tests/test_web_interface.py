from models import Availability, Service, db


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
            Availability(date="2026-10-15", time="10:00", is_available=True),
            Availability(date="2026-10-15", time="11:00", is_available=False),
        ])
        db.session.commit()

    response = client.get("/api/appointments/availability")

    assert response.status_code == 200
    assert response.get_json()["horarios"] == [{
        "id": 1,
        "date": "2026-10-15",
        "time": "10:00",
    }]


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
