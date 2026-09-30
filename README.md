# BeautySquad 1114 API

Backend educativo para un estudio de belleza. Permite registrar clientes, administrar servicios y controlar reservas de citas con Flask y SQLite.

## Inicio rápido

1. Crea y activa un entorno virtual.
2. Instala las dependencias de desarrollo: `pip install -r requirements-dev.txt`.
3. Configura las variables de entorno:

   ```bash
   export SECRET_KEY="replace-with-a-long-random-secret"
   export DATABASE_URL="sqlite:///beautysquad.db"
   ```

   Usa `.env.example` como guía. No subas secretos reales al repositorio.

4. Crea la base de datos mediante migraciones:

   ```bash
   flask --app app db upgrade
   ```

5. Crea el primer administrador desde la terminal:

   ```bash
   flask --app app create-admin
   ```

6. Inicia el servidor:

   ```bash
   python app.py
   ```

La API queda disponible en `http://127.0.0.1:5000`.

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
