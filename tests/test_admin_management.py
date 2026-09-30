from models import User, db


def create_admin(app):
    with app.app_context():
        admin = User(name="Admin", email="admin@example.com", role="admin")
        admin.set_password("secure-password")
        db.session.add(admin)
        db.session.commit()


def login(client, email, password="secure-password"):
    return client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )


def create_service(client):
    return client.post(
        "/api/services/",
        json={"name": "Brows", "description": "Basic", "price": 20},
    ).get_json()["servicio"]


def test_admin_can_update_and_delete_a_service(client, app):
    create_admin(app)
    login(client, "admin@example.com")
    service = create_service(client)

    response = client.patch(
        f"/api/services/{service['id']}",
        json={"name": "Premium brows", "price": 35},
    )

    assert response.status_code == 200
    assert response.get_json()["servicio"]["name"] == "Premium brows"
    assert response.get_json()["servicio"]["price"] == 35.0
    assert client.delete(f"/api/services/{service['id']}").status_code == 204
    assert client.get("/api/services/").get_json()["servicios"] == []


def test_admin_can_filter_appointments_and_see_context(client, app):
    create_admin(app)
    login(client, "admin@example.com")
    service = create_service(client)
    slot = {"date": "2026-10-10", "time": "09:00"}
    client.post("/api/appointments/availability", json=slot)

    client.post("/api/auth/logout")
    client.post(
        "/api/auth/register",
        json={"name": "Client", "email": "client@example.com", "password": "secure-password"},
    )
    login(client, "client@example.com")
    appointment = client.post(
        "/api/appointments/",
        json={**slot, "service_id": service["id"]},
    ).get_json()["cita"]

    client.post("/api/auth/logout")
    login(client, "admin@example.com")
    client.patch(
        f"/api/appointments/{appointment['id']}/status",
        json={"status": "confirmed"},
    )

    response = client.get("/api/appointments/?status=confirmed&date=2026-10-10")

    assert response.status_code == 200
    assert response.get_json()["citas"] == [{
        "id": appointment["id"],
        "date": "2026-10-10",
        "time": "09:00",
        "status": "confirmed",
        "user": {"id": 2, "name": "Client", "email": "client@example.com"},
        "service": {"id": service["id"], "name": "Brows", "price": 20.0},
    }]
