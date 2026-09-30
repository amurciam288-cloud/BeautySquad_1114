# BeautySquad 1114

## Backend

Backend desarrollado para el proyecto BeautySquad 1114.

El sistema permite gestionar usuarios, servicios y citas.

## Current security model

- Public registration always creates a `client` account.
- Login uses a Flask server-side session.
- Only an authenticated administrator can list users or create services.
- Clients can only list and create their own appointments.
- Administrators publish available appointment slots and can confirm or cancel appointments.

Create the first administrator from the terminal, never from the public API:

```bash
flask --app app create-admin
```

## Tecnologías

- Python
- Flask
- SQLite
- Flask-SQLAlchemy
- Werkzeug

## Funciones

- Registro de usuarios
- Inicio de sesión
- Cierre de sesión
- Roles de usuario
- Gestión de usuarios
- Gestión de servicios
- Gestión de citas
- Validación de información
- Base de datos
- Almacenamiento de información

## Instalación

Crear un entorno virtual:

python -m venv venv

Activar el entorno virtual en Windows:

venv\Scripts\activate

Instalar las dependencias:

pip install -r requirements.txt

Ejecutar el proyecto:

python app.py

## Tests

```bash
pytest
```

## Dirección

http://127.0.0.1:5000

## Endpoints

### Autenticación

POST /api/auth/register

POST /api/auth/login

POST /api/auth/logout

### Usuarios

GET /api/users/

### Servicios

GET /api/services/

POST /api/services/

### Citas

GET /api/appointments/

POST /api/appointments/

POST /api/appointments/availability

PATCH /api/appointments/<id>/status

## Objetivo

El objetivo es desarrollar el backend de BeautySquad permitiendo administrar usuarios, servicios y citas mediante una API conectada a una base de datos.
