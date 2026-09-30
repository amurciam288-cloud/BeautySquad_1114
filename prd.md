# PRD — BeautySquad 1114

## Propósito

BeautySquad es una plataforma educativa para un estudio de belleza. Su meta es que clientes consulten servicios y soliciten citas, mientras el personal administra la agenda de forma segura.

## Usuarios

| Usuario | Necesidad | Alcance actual |
| --- | --- | --- |
| Visitante | Consultar servicios y precios. | Disponible. |
| Cliente | Crear cuenta, iniciar sesión, reservar y consultar sus citas. | Disponible mediante interfaz web. |
| Administrador | Gestionar servicios, horarios y estados de citas. | Panel web básico disponible. |

## Objetivos del producto

1. Evitar reservas duplicadas mediante horarios publicados por un administrador.
2. Proteger la información y acciones administrativas mediante autenticación y roles.
3. Mantener precios y agenda en una base de datos versionada.
4. Construir una interfaz web sencilla sobre la API existente.

## Alcance entregado

### Clientes

- Registro público como cliente.
- Inicio y cierre de sesión.
- Consulta de servicios.
- Reserva de un horario publicado.
- Consulta de sus propias citas.
- Interfaz web para servicios, registro, login y reserva.

### Administración

- Creación inicial de administrador desde la terminal.
- Consulta de usuarios.
- Crear, editar y eliminar servicios sin citas asociadas.
- Publicar horarios disponibles.
- Consultar citas por fecha y estado.
- Confirmar, completar o cancelar citas según las transiciones permitidas.
- Panel web básico para publicar servicios, horarios y actualizar citas.

## Reglas de negocio

| Regla | Decisión |
| --- | --- |
| Rol público | El registro nunca crea administradores. |
| Propiedad | Un cliente no puede reservar ni consultar citas de otra persona. |
| Reserva | Solo se reserva un horario existente y disponible. |
| Duplicados | Fecha y hora de disponibilidad son únicas. |
| Cancelación | Cancelar una cita libera el horario. |
| Servicios | No se elimina un servicio que tenga citas asociadas. |
| Precio | Se persiste con dos decimales. |

## Fuera de alcance actual

- Perfil de cliente y edición/cancelación de citas por el cliente.
- Notificaciones, recordatorios, promociones, reseñas y redes sociales.
- Pagos y manejo de inventario.

## Próximas entregas

1. Mejorar el panel administrativo con edición visual y filtros.
2. Reglas de negocio adicionales: duración de servicios, múltiples profesionales y cancelación por cliente.
3. Notificaciones y componentes de marketing cuando el flujo principal esté validado.

## Criterios de éxito

- Un cliente no puede elevar sus permisos ni leer datos ajenos.
- Dos clientes no pueden ocupar el mismo horario.
- Un administrador puede mantener servicios, horarios y estados de citas.
- Las pruebas automatizadas validan el flujo antes de publicar cambios.
