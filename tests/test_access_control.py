def register(client, email="client@example.com", password="secure-password"):
    return client.post(
        "/api/auth/register",
        json={
            "name": "Client",
            "email": email,
            "password": password,
            "role": "admin",
        },
    )


def login(client, email="client@example.com", password="secure-password"):
    return client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )


def test_public_registration_cannot_create_an_admin(client):
    response = register(client)

    assert response.status_code == 201
    assert response.get_json()["usuario"]["role"] == "client"


def test_sensitive_routes_require_an_authenticated_user(client):
    assert client.get("/api/users/").status_code == 401
    assert client.post("/api/services/", json={"name": "Brows", "price": 20}).status_code == 401
    assert client.get("/api/appointments/").status_code == 401


def test_client_session_cannot_manage_services(client):
    register(client)
    assert login(client).status_code == 200

    response = client.post("/api/services/", json={"name": "Brows", "price": 20})

    assert response.status_code == 403
