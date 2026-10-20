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
    assert response.get_json()["servicio"]["price"] == "35.00"
    assert client.delete(f"/api/services/{service['id']}").status_code == 204
    assert client.get("/api/services/").get_json()["servicios"] == []


def test_admin_can_filter_appointments_and_see_context(client, app):
    create_admin(app)
    login(client, "admin@example.com")
    service = create_service(client)
    slot = {"date": "2026-10-30", "time": "09:00"}
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

    response = client.get("/api/appointments/?status=confirmed&date=2026-10-30")

    assert response.status_code == 200
    assert response.get_json()["citas"] == [{
        "id": appointment["id"],
        "date": "2026-10-30",
        "time": "09:00",
        "status": "confirmed",
        "user": {"id": 2, "name": "Client", "email": "client@example.com"},
        "service": {"id": service["id"], "name": "Brows", "price": "20.00"},
    }]


def test_client_appointment_response_includes_own_service_without_client_context(client, app):
    create_admin(app)
    login(client, "admin@example.com")
    service = create_service(client)
    own_slot = {"date": "2026-10-30", "time": "09:00"}
    other_slot = {"date": "2026-10-30", "time": "10:00"}
    client.post("/api/appointments/availability", json=own_slot)
    client.post("/api/appointments/availability", json=other_slot)

    client.post("/api/auth/logout")
    client.post(
        "/api/auth/register",
        json={"name": "Client", "email": "client@example.com", "password": "secure-password"},
    )
    login(client, "client@example.com")
    own_appointment = client.post(
        "/api/appointments/",
        json={**own_slot, "service_id": service["id"]},
    ).get_json()["cita"]

    client.post("/api/auth/logout")
    client.post(
        "/api/auth/register",
        json={"name": "Other Client", "email": "other@example.com", "password": "secure-password"},
    )
    login(client, "other@example.com")
    client.post("/api/appointments/", json={**other_slot, "service_id": service["id"]})

    client.post("/api/auth/logout")
    login(client, "client@example.com")

    response = client.get("/api/appointments/")

    assert response.status_code == 200
    assert response.get_json()["citas"] == [{
        "id": own_appointment["id"],
        "date": "2026-10-30",
        "time": "09:00",
        "status": "pending",
        "service": {"id": service["id"], "name": "Brows", "price": "20.00"},
    }]


def test_client_appointments_ui_renders_service_context_and_cancellation_action(client):
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert b"appointment.service.name" in response.data
    assert b"appointment.service.price" in response.data
    assert b'data-client-cancel' in response.data
