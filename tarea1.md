# Tarea 1 — Ejecutar y probar BeautySquad localmente

## Objetivo

Clonar el proyecto, ejecutarlo en tu computador y comprobar el flujo completo: administrador publica un servicio y horario; cliente reserva una cita; administrador confirma la cita.

## Entrega

Envía:

- Una captura de `pytest -q` con las pruebas aprobadas.
- Una captura de la página de reserva con una cita creada.
- Una explicación breve: ¿por qué un registro público no puede crear un administrador?

## 1. Requisitos

- Git instalado.
- Python 3 instalado.
- Una terminal: PowerShell en Windows, o Terminal en macOS/Linux.

Comprueba las versiones:

```bash
git --version
python --version
```

En macOS o Linux, si `python` no funciona, usa `python3` en los comandos siguientes.

## 2. Clonar el proyecto

```bash
git clone https://github.com/amurciam288-cloud/BeautySquad_1114.git
cd BeautySquad_1114
```

## 3. Crear y activar el entorno virtual

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS o Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Al activarlo, la terminal mostrará `(.venv)` al inicio de la línea.

## 4. Instalar dependencias

```bash
pip install -r requirements-dev.txt
```

## 5. Configurar variables de entorno

Estas variables se usan solo para tu entorno local. No subas secretos reales a GitHub.

### Windows PowerShell

```powershell
$env:SECRET_KEY = "clave-local-para-pruebas"
$env:DATABASE_URL = "sqlite:///beautysquad.db"
```

### macOS o Linux

```bash
export SECRET_KEY="clave-local-para-pruebas"
export DATABASE_URL="sqlite:///beautysquad.db"
```

## 6. Crear la base de datos

```bash
flask --app app db upgrade
```

Este comando aplica las migraciones. No uses `db.create_all()`.

## 7. Crear el primer administrador

```bash
flask --app app create-admin
```

La terminal pedirá nombre, correo y contraseña. Guarda estos datos: los necesitarás para entrar al panel de administración.

## 8. Ejecutar la aplicación

```bash
python app.py
```

Abre en el navegador: <http://127.0.0.1:5000>

Para detener el servidor, vuelve a la terminal y presiona `Ctrl + C`.

## 9. Probar el flujo principal

### A. Como administrador

1. Entra a `/login` con el administrador creado en el paso 7.
2. Abre **Administración**.
3. Crea un servicio, por ejemplo: `Diseño de cejas`, precio `25000`.
4. Publica un horario futuro, por ejemplo una fecha posterior a hoy a las `10:00`.
5. Cierra sesión.

### B. Como cliente

1. Entra a **Regístrate** y crea una cuenta nueva.
2. Inicia sesión con esa cuenta.
3. Abre **Reservar**.
4. Selecciona el servicio y el horario publicados.
5. Confirma la reserva.
6. Comprueba que la cita aparece en **Mis citas**.

### C. Confirmar la cita

1. Cierra la sesión del cliente.
2. Entra otra vez con el administrador.
3. Abre **Administración**.
4. Confirma la cita en la tabla.

## 10. Ejecutar las pruebas automáticas

Con el entorno virtual activo, ejecuta:

```bash
pytest -q
```

El resultado esperado es que todas las pruebas terminen en `passed`.

## Checklist antes de entregar

- [ ] El proyecto fue clonado en mi computador.
- [ ] El entorno virtual está activo.
- [ ] Apliqué las migraciones.
- [ ] Creé un administrador desde la terminal.
- [ ] Creé un servicio y un horario futuro.
- [ ] Un cliente reservó una cita.
- [ ] El administrador confirmó la cita.
- [ ] `pytest -q` terminó correctamente.
- [ ] No subí `.venv`, la base de datos ni secretos al repositorio.

## Si algo falla

| Problema | Revisión rápida |
| --- | --- |
| `python` no se reconoce | Prueba `python3` o `py`. |
| `flask` no se reconoce | Activa `.venv` e instala dependencias otra vez. |
| Error de base de datos | Confirma que ejecutaste `flask --app app db upgrade`. |
| No puedo reservar | Verifica que el administrador creó un servicio y un horario futuro disponible. |
| No aparece Administración | Inicia sesión con la cuenta creada mediante `create-admin`, no con un registro público. |
