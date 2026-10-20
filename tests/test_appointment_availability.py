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


def register(client, email):
    return client.post(
        "/api/auth/register",
        json={"name": "Client", "email": email, "password": "secure-password"},
    )


def create_service(client):
    response = client.post(
        "/api/services/",
        json={"name": "Brows", "price": 20},
    )
    return response.get_json()["servicio"]["id"]


def test_client_can_only_book_a_published_available_slot(client, app):
    create_admin(app)
    login(client, "admin@example.com")
    service_id = create_service(client)

    slot = {"date": "2026-10-05", "time": "10:30"}
    assert client.post("/api/appointments/availability", json=slot).status_code == 201

    client.post("/api/auth/logout")
    register(client, "first@example.com")
    login(client, "first@example.com")

    booking = {**slot, "service_id": service_id}
    assert client.post("/api/appointments/", json=booking).status_code == 201

    client.post("/api/auth/logout")
    register(client, "second@example.com")
    login(client, "second@example.com")
    assert client.post("/api/appointments/", json=booking).status_code == 409


def test_admin_cancellation_reopens_the_slot(client, app):
    create_admin(app)
    login(client, "admin@example.com")
    service_id = create_service(client)
    slot = {"date": "2026-10-06", "time": "11:00"}
    client.post("/api/appointments/availability", json=slot)

    client.post("/api/auth/logout")
    register(client, "client@example.com")
    login(client, "client@example.com")
    appointment = client.post(
        "/api/appointments/",
        json={**slot, "service_id": service_id},
    ).get_json()["cita"]

    client.post("/api/auth/logout")
    login(client, "admin@example.com")
    response = client.patch(
        f"/api/appointments/{appointment['id']}/status",
        json={"status": "cancelled"},
    )

    assert response.status_code == 200

    client.post("/api/auth/logout")
    login(client, "client@example.com")
    assert client.post(
        "/api/appointments/",
        json={**slot, "service_id": service_id},
    ).status_code == 201


def test_client_can_cancel_own_pending_appointment_and_reopen_slot(client, app):
    create_admin(app)
    login(client, "admin@example.com")
    service_id = create_service(client)
    slot = {"date": "2026-11-06", "time": "11:00"}
    client.post("/api/appointments/availability", json=slot)

    client.post("/api/auth/logout")
    register(client, "client@example.com")
    login(client, "client@example.com")
    appointment = client.post(
        "/api/appointments/",
        json={**slot, "service_id": service_id},
    ).get_json()["cita"]

    response = client.patch(
        f"/api/appointments/{appointment['id']}/status",
        json={"status": "cancelled"},
    )

    assert response.status_code == 200
    assert response.get_json()["cita"]["status"] == "cancelled"
    assert client.get("/api/appointments/availability").get_json()["horarios"] == [{
        "id": 1,
        **slot,
    }]


def test_client_can_cancel_own_confirmed_appointment(client, app):
    create_admin(app)
    login(client, "admin@example.com")
    service_id = create_service(client)
    slot = {"date": "2026-11-07", "time": "11:00"}
    client.post("/api/appointments/availability", json=slot)

    client.post("/api/auth/logout")
    register(client, "client@example.com")
    login(client, "client@example.com")
    appointment = client.post(
        "/api/appointments/",
        json={**slot, "service_id": service_id},
    ).get_json()["cita"]

    client.post("/api/auth/logout")
    login(client, "admin@example.com")
    assert client.patch(
        f"/api/appointments/{appointment['id']}/status",
        json={"status": "confirmed"},
    ).status_code == 200

    client.post("/api/auth/logout")
    login(client, "client@example.com")
    response = client.patch(
        f"/api/appointments/{appointment['id']}/status",
        json={"status": "cancelled"},
    )

    assert response.status_code == 200


def test_client_cannot_cancel_another_clients_appointment(client, app):
    create_admin(app)
    login(client, "admin@example.com")
    service_id = create_service(client)
    slot = {"date": "2026-11-08", "time": "11:00"}
    client.post("/api/appointments/availability", json=slot)

    client.post("/api/auth/logout")
    register(client, "first@example.com")
    login(client, "first@example.com")
    appointment = client.post(
        "/api/appointments/",
        json={**slot, "service_id": service_id},
    ).get_json()["cita"]

    client.post("/api/auth/logout")
    register(client, "second@example.com")
    login(client, "second@example.com")
    response = client.patch(
        f"/api/appointments/{appointment['id']}/status",
        json={"status": "cancelled"},
    )

    assert response.status_code == 403
    assert client.get("/api/appointments/availability").get_json()["horarios"] == []


def test_client_cannot_cancel_appointment_outside_allowed_statuses(client, app):
    create_admin(app)
    login(client, "admin@example.com")
    service_id = create_service(client)
    slot = {"date": "2026-11-09", "time": "11:00"}
    client.post("/api/appointments/availability", json=slot)

    client.post("/api/auth/logout")
    register(client, "client@example.com")
    login(client, "client@example.com")
    appointment = client.post(
        "/api/appointments/",
        json={**slot, "service_id": service_id},
    ).get_json()["cita"]

    client.post("/api/auth/logout")
    login(client, "admin@example.com")
    assert client.patch(
        f"/api/appointments/{appointment['id']}/status",
        json={"status": "confirmed"},
    ).status_code == 200
    assert client.patch(
        f"/api/appointments/{appointment['id']}/status",
        json={"status": "completed"},
    ).status_code == 200

    client.post("/api/auth/logout")
    login(client, "client@example.com")
    response = client.patch(
        f"/api/appointments/{appointment['id']}/status",
        json={"status": "cancelled"},
    )

    assert response.status_code == 400
