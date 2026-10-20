from datetime import date, timedelta

from models import User, db


def future_date():
    return (date.today() + timedelta(days=30)).isoformat()


def login(client, email):
    return client.post(
        "/api/auth/login",
        json={"email": email, "password": "secure-password"},
    )


def prepare_appointment(client, app, email="client@example.com"):
    with app.app_context():
        admin = User(name="Admin", email="admin@example.com", role="admin")
        admin.set_password("secure-password")
        db.session.add(admin)
        db.session.commit()

    login(client, "admin@example.com")
    service = client.post(
        "/api/services/",
        json={"name": "Brows", "price": 20},
    ).get_json()["servicio"]
    slot = {"date": future_date(), "time": "10:30"}
    client.post("/api/appointments/availability", json=slot)
    client.post("/api/auth/logout")
    client.post(
        "/api/auth/register",
        json={"name": "Client", "email": email, "password": "secure-password"},
    )
    login(client, email)
    appointment = client.post(
        "/api/appointments/",
        json={**slot, "service_id": service["id"]},
    ).get_json()["cita"]
    return appointment


def test_client_can_record_each_supported_simulated_payment(client, app):
    appointment = prepare_appointment(client, app)

    response = client.post(
        f"/api/appointments/{appointment['id']}/payment",
        json={"method": "tarjeta_simulada"},
    )

    assert response.status_code == 201
    payment = response.get_json()["pago"]
    assert payment["status"] == "simulated_success"
    assert payment["method"] == "tarjeta_simulada"
    assert payment["reference"].startswith("SIM-")
    assert response.get_json()["cita"]["status"] == "pending"
    assert "card" not in payment
    assert "cvv" not in payment


def test_payment_rejects_duplicate_invalid_and_nonexistent_appointments(client, app):
    appointment = prepare_appointment(client, app)
    endpoint = f"/api/appointments/{appointment['id']}/payment"

    assert client.post(endpoint, json={"method": "card"}).status_code == 400
    assert client.post(endpoint, json={"method": "pse_simulado"}).status_code == 201
    assert client.post(endpoint, json={"method": "efectivo_simulado"}).status_code == 409
    assert client.post("/api/appointments/999/payment", json={"method": "card"}).status_code == 404


def test_other_client_cannot_record_payment_for_an_appointment(client, app):
    appointment = prepare_appointment(client, app)
    client.post("/api/auth/logout")
    client.post(
        "/api/auth/register",
        json={"name": "Other", "email": "other@example.com", "password": "secure-password"},
    )
    login(client, "other@example.com")

    response = client.post(
        f"/api/appointments/{appointment['id']}/payment",
        json={"method": "efectivo_simulado"},
    )

    assert response.status_code == 403


def test_admin_can_record_payment_without_changing_appointment_status(client, app):
    appointment = prepare_appointment(client, app)
    client.post("/api/auth/logout")
    login(client, "admin@example.com")

    response = client.post(
        f"/api/appointments/{appointment['id']}/payment",
        json={"method": "pse_simulado"},
    )

    assert response.status_code == 201
    assert response.get_json()["cita"]["status"] == "pending"
    assert client.get("/api/appointments/").get_json()["citas"][0]["payment"]["method"] == "pse_simulado"
