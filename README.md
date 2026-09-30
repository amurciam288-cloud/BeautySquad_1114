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
- Administrators can edit or remove services that have no associated appointments.

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

Before running the project, configure the environment variables. Copy
`.env.example` and export values in your terminal; do not commit a real secret.

```bash
export SECRET_KEY="replace-with-a-long-random-secret"
export DATABASE_URL="sqlite:///beautysquad.db"
```

Crear un entorno virtual:

python -m venv venv

Activar el entorno virtual en Windows:

venv\Scripts\activate

Instalar las dependencias:

pip install -r requirements.txt

Ejecutar el proyecto:

python app.py

## Database migrations

The project uses Flask-Migrate. Run these commands after installing dependencies:

```bash
flask --app app db upgrade
```

When the data model changes, create and apply a new migration:

```bash
flask --app app db migrate -m "describe the change"
flask --app app db upgrade
```

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

PATCH /api/services/<id>

DELETE /api/services/<id>

### Citas

GET /api/appointments/

POST /api/appointments/

POST /api/appointments/availability

PATCH /api/appointments/<id>/status

## Objetivo

El objetivo es desarrollar el backend de BeautySquad permitiendo administrar usuarios, servicios y citas mediante una API conectada a una base de datos.
