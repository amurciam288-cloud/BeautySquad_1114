# BeautySquad 1114

## Backend

Backend desarrollado para el proyecto BeautySquad 1114.

El sistema permite gestionar usuarios, servicios y citas.

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

## Objetivo

El objetivo es desarrollar el backend de BeautySquad permitiendo administrar usuarios, servicios y citas mediante una API conectada a una base de datos.
