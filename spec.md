# Especificación técnica - BeautySquad1114
# Especificación técnica - BeautySquad1114

## 1. Descripción

BeautySquad1114 será una página web para un estudio de belleza y estética. La página permitirá mostrar los servicios, sus precios e información importante del estudio.

También tendrá un sistema de usuarios y citas para que los clientes puedan registrarse, iniciar sesión y solicitar una cita.

El proyecto será realizado con Python y Flask, utilizando HTML, CSS y JavaScript para la parte visual e interactiva. Para guardar la información se utilizará una base de datos SQLite.

---

## 2. Tecnologías

Las tecnologías que utilizaremos son:

* **Python:** para desarrollar la parte principal del sistema.
* **Flask:** para crear y manejar la página web.
* **HTML:** para crear la estructura de las páginas.
* **CSS:** para los estilos y el diseño.
* **JavaScript:** para agregar algunas funciones e interacciones.
* **SQLite:** para guardar la información.
* **SQLAlchemy:** para conectar Python con la base de datos.
* **Git:** para guardar y controlar los cambios del proyecto.
* **GitHub:** para trabajar en equipo y almacenar el proyecto.

---

## 3. Organización MVC

El proyecto utilizará la arquitectura **MVC (Modelo, Vista y Controlador)**.

La idea es separar el proyecto en diferentes partes para que sea más fácil organizarlo.

### Modelo

Se encargará de manejar los datos y la información que se guarda en la base de datos.

Los principales datos serán:

* Usuarios.
* Servicios.
* Citas.
* Horarios.

### Vista

Será la parte que verá el usuario cuando entre a la página.

Aquí estarán las páginas de:

* Inicio.
* Servicios.
* Registro.
* Inicio de sesión.
* Citas.
* Perfil.
* Panel del administrador.

### Controlador

Se encargará de recibir las acciones del usuario y hacer que la Vista y el Modelo trabajen juntos.

Por ejemplo, cuando un cliente solicite una cita, el controlador recibirá los datos y los enviará a la base de datos para guardarlos.

---

## 4. Estructura del proyecto

La estructura inicial será:

```text
BeautySquad1114/
│
├── app/
│   ├── models/
│   ├── views/
│   ├── controllers/
│   ├── templates/
│   └── static/
│
├── database/
├── tests/
├── requirements.txt
├── config.py
├── run.py
├── PRD.md
├── spec.md
└── README.md
```

### Carpetas principales

**models:** tendrá los archivos relacionados con los datos.

**views:** tendrá las partes relacionadas con las vistas del sistema.

**controllers:** tendrá la lógica que conecta las diferentes partes.

**templates:** tendrá las páginas HTML.

**static:** tendrá los archivos CSS, JavaScript e imágenes.

**database:** tendrá la información relacionada con la base de datos.

**tests:** se utilizará para realizar pruebas del proyecto.

---

## 5. Usuarios

La página tendrá dos tipos principales de usuarios:

### Cliente

El cliente podrá:

* Crear una cuenta.
* Iniciar sesión.
* Cerrar sesión.
* Ver los servicios.
* Ver los precios.
* Consultar horarios.
* Solicitar citas.
* Ver sus citas.
* Cancelar o modificar una cita cuando sea posible.
* Ver la información de contacto y redes sociales.

### Administrador

El administrador podrá:

* Iniciar sesión.
* Ver los clientes.
* Agregar servicios.
* Modificar servicios.
* Eliminar servicios.
* Ver las citas.
* Confirmar citas.
* Cancelar citas.
* Administrar los horarios disponibles.

---

## 6. Servicios

La página mostrará los diferentes servicios que ofrece BeautySquad1114.

Entre ellos estarán:

* Diseño de cejas.
* Pigmentación de cejas.
* Servicios para pestañas.
* Pigmentación de labios.
* Procedimientos estéticos de labios.
* Preparación y mezcla de pigmentos.
* Otros servicios que se puedan agregar después.

Cada servicio tendrá información como:

* Nombre.
* Descripción.
* Precio.
* Disponibilidad.

El administrador será el encargado de agregar, modificar o eliminar los servicios.

---

## 7. Sistema de citas

Una de las funciones principales será permitir que los clientes puedan solicitar citas.

El proceso será:

1. El cliente inicia sesión.
2. Entra a la sección de servicios.
3. Selecciona el servicio que desea.
4. Consulta los horarios disponibles.
5. Escoge una fecha y hora.
6. Solicita la cita.
7. La cita queda registrada.
8. El administrador puede confirmarla o cancelarla.

Los estados de una cita podrán ser:

* Pendiente.
* Confirmada.
* Cancelada.
* Finalizada.

El sistema deberá revisar que el horario seleccionado esté disponible.

---

## 8. Base de datos

Se utilizará **SQLite** para guardar la información del proyecto.

La base de datos tendrá principalmente las siguientes tablas:

### Usuarios

Guardará los datos de los usuarios.

* ID.
* Nombre.
* Correo.
* Contraseña.
* Rol.

### Servicios

Guardará la información de cada servicio.

* ID.
* Nombre.
* Descripción.
* Precio.
* Estado.

### Citas

Guardará las citas realizadas.

* ID.
* Usuario.
* Servicio.
* Fecha.
* Hora.
* Estado.

### Horarios

Guardará los horarios disponibles.

* ID.
* Fecha.
* Hora.
* Disponibilidad.

---

## 9. Registro e inicio de sesión

Los usuarios podrán crear una cuenta mediante un formulario de registro.

Para iniciar sesión deberán ingresar su correo y contraseña.

Después de iniciar sesión, el sistema identificará si se trata de un cliente o un administrador.

Cada usuario podrá acceder solamente a las funciones que correspondan a su tipo de cuenta.

Por ejemplo, un cliente no podrá entrar al panel de administración.

---

## 10. Páginas de la página web

Las principales páginas serán:

### Inicio

Tendrá una presentación de BeautySquad1114, algunos servicios destacados, información del estudio y botones para reservar o contactar.

### Servicios

Mostrará los servicios disponibles, sus precios y una descripción.

### Registro

Permitirá crear una cuenta.

### Inicio de sesión

Permitirá entrar al sistema.

### Citas

Permitirá a los clientes solicitar y consultar sus citas.

### Perfil

Mostrará información básica del usuario.

### Panel administrativo

Permitirá al administrador gestionar servicios, citas y horarios.

---

## 11. Diseño

El diseño de la página estará relacionado con la belleza y la estética.

Se buscará que sea:

* Moderno.
* Bonito.
* Ordenado.
* Fácil de utilizar.
* Atractivo para los clientes.

Se utilizarán HTML y CSS para crear el diseño y JavaScript cuando sea necesario para agregar interacciones.

También se buscará que la página pueda verse correctamente en computador y celular.

---

## 12. Marketing digital

La página también tendrá elementos para promocionar BeautySquad1114.

Se podrán incluir:

* Redes sociales.
* Fotografías de los servicios.
* Promociones.
* Descuentos.
* Novedades.
* Botones de contacto.
* Botones para reservar citas.

Esto ayudará a que los visitantes conozcan mejor el estudio y puedan comunicarse con él.

---

## 13. Validaciones

El sistema tendrá algunas validaciones para evitar errores.

Por ejemplo:

* No permitir campos obligatorios vacíos.
* Revisar que el correo tenga un formato correcto.
* Evitar registros con un correo que ya exista.
* Revisar los datos del inicio de sesión.
* Comprobar que el horario esté disponible.
* Evitar que un cliente pueda acceder a funciones del administrador.

---

## 14. Seguridad

Para proteger la información del sistema se tendrá en cuenta:

* Uso de inicio de sesión.
* Diferentes permisos según el tipo de usuario.
* Protección del panel administrativo.
* Validación de los datos ingresados.
* Manejo adecuado de las contraseñas.

---

## 15. Flujo principal

El funcionamiento principal de la página será:

```text
Entrar a BeautySquad1114
          ↓
     Ver servicios
          ↓
     Registrarse
          ↓
    Iniciar sesión
          ↓
   Elegir un servicio
          ↓
   Consultar horarios
          ↓
    Solicitar cita
          ↓
 Administrador revisa
          ↓
Confirmar o cancelar cita
```

---

## 16. Pruebas

Durante el desarrollo se realizarán pruebas para comprobar que las funciones funcionen correctamente.

Se probará:

* Registro de usuarios.
* Inicio de sesión.
* Cierre de sesión.
* Visualización de servicios.
* Creación de citas.
* Consulta de citas.
* Cancelación de citas.
* Gestión de servicios.
* Gestión de horarios.
* Acceso del administrador.

---

## 17. Git y GitHub

Git y GitHub serán utilizados para trabajar en equipo y guardar los cambios del proyecto.

Cada integrante podrá trabajar en las partes que le correspondan y luego subir sus cambios al repositorio.

Se utilizarán:

* Commits para guardar cambios.
* Ramas cuando sea necesario.
* Pull Requests para unir cambios.
* GitHub para almacenar el proyecto.

---

## 18. Requisitos para utilizar el proyecto

Para trabajar en el proyecto será necesario tener:

* Python instalado.
* Git instalado.
* Un editor de código.
* Flask y las demás dependencias instaladas.
* El repositorio de GitHub.

Los pasos completos para instalar y ejecutar el proyecto se explicarán posteriormente en el `README.md`.

---

## 19. Mejoras futuras

En el futuro se podrían agregar:

* Recordatorios de citas.
* Notificaciones.
* Galería de trabajos.
* Reseñas de clientes.
* Calificaciones.
* Historial de citas.
* Más promociones.
* Más servicios.
* Mejoras en el panel administrativo.

---

## 20. Estado del proyecto

**Estado:** En desarrollo.

BeautySquad1114 se encuentra en etapa de planificación y desarrollo. Las diferentes funciones se irán agregando y probando durante el avance del proyecto.

---

## 21. Equipo

**Proyecto:** BeautySquad1114
**Sección:** 1114

**Integrantes:**

* Integrante 1  alisson 
* Integrante 2  liseth
* Integrante 3  angie
* Integrante 4  cathalina
