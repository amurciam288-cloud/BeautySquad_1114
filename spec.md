# Especificación técnica — BeautySquad 1114

## Arquitectura actual

BeautySquad combina una API Flask con una interfaz web inicial. Las rutas JSON sostienen las páginas de servicios, autenticación, reservas y administración básica.

```text
BeautySquad_1114/
├── app.py                  # Fábrica Flask, blueprints y comando create-admin
├── config.py               # SECRET_KEY y DATABASE_URL desde entorno
├── models.py               # SQLAlchemy: User, Service, Availability, Appointment
├── routes/
│   ├── auth.py             # Registro, login y logout
│   ├── security.py         # Decoradores login_required y admin_required
│   ├── users.py            # Consulta administrativa de usuarios
│   ├── services.py         # Catálogo y administración de servicios
│   └── appointments.py     # Horarios, reservas, filtros y estados
├── templates/              # Páginas HTML de cliente y administración
├── static/                 # Estilos y comportamiento del navegador
├── migrations/             # Alembic / Flask-Migrate
├── tests/                  # Pruebas pytest
├── .env.example            # Plantilla de configuración
├── requirements.txt
├── prd.md
└── README.md
```

## Tecnologías

| Tecnología | Uso |
| --- | --- |
| Python + Flask | API y sesiones. |
| Flask-SQLAlchemy | Persistencia y relaciones. |
| Flask-Migrate | Versionado del esquema. |
| SQLite | Base de datos local. |
| Werkzeug | Hash de contraseñas. |
| pytest | Pruebas automatizadas. |

## Seguridad y autorización

1. `POST /api/auth/register` crea siempre usuarios con rol `client`.
2. `POST /api/auth/login` almacena `user_id` en la sesión Flask tras comprobar la contraseña hasheada.
3. `login_required` recupera el usuario de la base de datos en cada solicitud protegida.
4. `admin_required` exige sesión válida y rol `admin`.
5. El primer administrador se crea con `flask --app app create-admin`.

## Modelo de datos

| Entidad | Campos principales | Reglas |
| --- | --- | --- |
| User | name, email, password_hash, role | email único; roles `client` o `admin`. |
| Service | name, description, price | precio `Numeric(10,2)`. |
| Availability | date, time, is_available | combinación fecha/hora única. |
| Appointment | date, time, status, user_id, service_id | pertenece a un cliente y servicio. |

## Flujo de citas

1. Un administrador publica un horario con fecha `YYYY-MM-DD` y hora `HH:MM`.
2. Un cliente autenticado selecciona servicio y horario.
3. La API confirma que el horario existe y está disponible.
4. La reserva marca el horario como no disponible y crea la cita en estado `pending`.
5. El administrador puede confirmar, completar o cancelar según el estado actual.
6. Una cancelación vuelve a habilitar el horario.

## API y respuesta por rol

| Recurso | Cliente | Administrador |
| --- | --- | --- |
| Usuarios | Sin acceso. | Lista de usuarios. |
| Servicios | Consulta pública. | CRUD, excepto borrar con citas. |
| Citas | Solo sus citas. | Todas las citas, filtros `status` y `date`, con contexto de cliente y servicio. |
| Horarios | Se consumen al reservar. | Se publican. |

## Configuración y migraciones

- `SECRET_KEY` firma sesiones. Debe cambiarse en cada entorno real.
- `DATABASE_URL` define la conexión; por defecto usa SQLite local.
- La migración inicial es `fbd3966caad0_create_core_tables.py`.
- Para aplicar el esquema: `flask --app app db upgrade`.
- Para evolucionarlo: `flask --app app db migrate -m "mensaje"` y luego `db upgrade`.

## Calidad

Ejecutar `pytest -q` antes de crear un commit. La suite actual cubre permisos, reservas, cancelaciones, gestión administrativa, configuración y dinero decimal.

## Limitaciones conocidas

- La interfaz es inicial: no incluye perfil, edición visual de servicios ni calendario avanzado.
- SQLite es apropiada para aprendizaje y desarrollo local; una publicación multiusuario requerirá una base de datos de servidor.
- No hay duración de servicios, profesionales ni zonas horarias.
- Los clientes todavía no pueden cancelar o modificar sus propias citas.
