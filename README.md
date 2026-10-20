# BeautySquad 1114 API

Backend educativo para un estudio de belleza. Permite registrar clientes, administrar servicios y controlar reservas de citas con Flask y SQLite.

## Uso local en Windows 11

Estas instrucciones están pensadas para las alumnas que trabajan con **Windows 11**, **CMD** y, opcionalmente, **Visual Studio Code**.

### 1. Instalar los requisitos

Instala:

- Python 3.11 o superior desde <https://www.python.org/downloads/>.
- Git desde <https://git-scm.com/download/win>.
- Visual Studio Code desde <https://code.visualstudio.com/> (opcional).

Durante la instalación de Python, activa la opción **Add Python to PATH**.

Comprueba la instalación en CMD:

```cmd
python --version
git --version
```

### 2. Descargar el proyecto

En CMD, ve a la carpeta donde guardarás el proyecto y clónalo:

```cmd
git clone https://github.com/amurciam288-cloud/BeautySquad_1114.git
cd BeautySquad_1114
```

Si ya tienes el proyecto, actualízalo así:

```cmd
git pull
```

### 3. Abrirlo en Visual Studio Code (opcional)

Desde la carpeta del proyecto ejecuta:

```cmd
code .
```

En VS Code, abre una terminal con **Terminal > New Terminal** y selecciona **Command Prompt** si deseas continuar usando CMD.

### 4. Crear y activar el entorno virtual

En la terminal CMD ubicada dentro del proyecto:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Cuando esté activo, aparecerá `(.venv)` al comienzo de la línea de comandos.

### 5. Instalar las dependencias

```cmd
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### 6. Configurar la aplicación en CMD

Estas variables solo estarán activas en la ventana actual de CMD:

```cmd
set SECRET_KEY=beautysquad-clave-local-1114
set DATABASE_URL=sqlite:///beautysquad.db
```

No compartas claves reales ni las subas al repositorio.

### 7. Crear o actualizar la base de datos

```cmd
flask --app app db upgrade
```

### 8. Crear la cuenta administradora

```cmd
flask --app app create-admin
```

El programa solicitará nombre, correo, contraseña y confirmación de contraseña.

### 9. Iniciar el proyecto

```cmd
python app.py
```

No cierres esta ventana de CMD mientras uses la aplicación. Abre el navegador en:

- Inicio: <http://127.0.0.1:5000>
- Registro: <http://127.0.0.1:5000/register>
- Inicio de sesión: <http://127.0.0.1:5000/login>
- Reservas: <http://127.0.0.1:5000/bookings>
- Administración: <http://127.0.0.1:5000/admin>

### 10. Preparar una cita de prueba

Para que aparezcan opciones en **Reservar una cita**:

1. Entra a `/login` con la cuenta administradora.
2. Abre `/admin`.
3. Crea al menos un servicio.
4. Publica un horario futuro.
5. Cierra sesión.
6. Registra una cuenta de cliente en `/register`.
7. Inicia sesión como cliente.
8. Abre `/bookings` y reserva el servicio y horario disponibles.

Si los selectores muestran `Cargando...`, confirma que el servidor sigue ejecutándose en CMD y que abriste la aplicación desde `http://127.0.0.1:5000`, no desde un archivo HTML con doble clic.

## Qué está implementado

| Área | Comportamiento actual |
| --- | --- |
| Registro | Toda cuenta pública nace con el rol `client`. |
| Sesión | Login guarda una sesión de Flask; logout la elimina. |
| Servicios | Cualquier visitante los consulta; solo admin los crea, edita o elimina. |
| Horarios | Solo admin publica horarios disponibles. |
| Citas | Un cliente reserva únicamente horarios publicados y disponibles. |
| Estados | `pending → confirmed/cancelled`; `confirmed → completed/cancelled`. |
| Interfaz | Páginas para servicios, autenticación, reserva y administración básica. |
| Base de datos | SQLite, SQLAlchemy y Flask-Migrate; precios `Numeric(10,2)`. |

## Endpoints

| Método | Ruta | Acceso |
| --- | --- | --- |
| POST | `/api/auth/register` | Público |
| POST | `/api/auth/login` | Público |
| POST | `/api/auth/logout` | Público; elimina la sesión si existe |
| GET | `/api/users/` | Admin |
| GET | `/api/services/` | Público |
| POST | `/api/services/` | Admin |
| PATCH | `/api/services/<id>` | Admin |
| DELETE | `/api/services/<id>` | Admin; sin citas asociadas |
| GET | `/api/appointments/?status=&date=` | Cliente: propias; admin: todas |
| POST | `/api/appointments/` | Cliente autenticado |
| POST | `/api/appointments/availability` | Admin |
| PATCH | `/api/appointments/<id>/status` | Admin |

## Pruebas

```bash
pytest -q
```

Las pruebas cubren registro seguro, sesiones, permisos, disponibilidad de horarios, cancelación, administración, configuración y precisión monetaria.

## Migraciones

Cuando cambies los modelos, genera y aplica una migración nueva:

```bash
flask --app app db migrate -m "describe the change"
flask --app app db upgrade
```

No se usa `db.create_all()` al iniciar la aplicación: las migraciones son la fuente de verdad para el esquema.

## Próximo alcance

La edición o cancelación de citas por clientes, notificaciones, marketing y redes sociales todavía no están implementados. Están documentados como trabajo futuro en `prd.md` y `spec.md`.
