# 📝 Historial de Cambios (Changelog)

Todos los cambios notables en este proyecto serán documentados en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [1.4.1] - 2026-06-04

### 🛠️ Cambios

- Se cambió en las plantillas de email el texto "Código QR" por "Código de Acceso".
- Se cambió en las plantillas de email el texto "Código de Barras" por "Código de Asistencia".
- Se pasó el tiempo de expiración para volver a ser otro intento de registro y cambios de contraseña de los clientes de 48 horas a 24 horas.

## [1.4.0] - 2026-05-29

### ✨ Mejoras

- Mantener en mis citas, también las marcadas con estado "ASISTIO" para que pueda salir el cliente con el mismo QR.
- Al entregar las citas agendadas de un cliente, solo se entregan las que son de hoy en adelante, están en estado de Pendiente y activas.
- Validar el campo booleano `oficinas.puede_enviar_qr` para incluir el código QR y código de barras de asistencia en los emails al crear una cita.
- Mejorado el mensaje de error al fallar la generación del código de barras de asistencia.
- Añadido el código de barras de asistencia a la plantilla de cita creada.
- Nuevo servicio para creación de un código de barras para identificar la cita. Con esto se podrá marcar la asistencia del cliente y añadirlo al sistema de turnos.

### ❌ Eliminado

- Se quitó el código de asistencia en la plantilla de cita creada. Será remplazado por el código de barras de asistencia en su lugar.

### ⚙️ Requerimientos

- Actualización de BD, ejecutar _scripts_ de migración con `psql -f [nombre_archivo.sql]`:
    - `v1.4.0-01-anadir-campo-codigo_barras.sql`.

- Añadir paquetes de librerías con `uv add [lib]`:
    - `python-barcode pillow`
    - `google-cloud-storage`

- Añadir nuevas variables de entorno:
    - `GOOGLE_APPLICATION_CREDENTIALS`
    - `GCS_BUCKET_NAME`


## [1.3.0] - 2026-05-22

### ✨ Mejoras

- Añadido campo `instrucciones` al modelo `cit_servicios` y añadirlo en la entrega de su _endpoint_.
- Mensaje de requisitos en plantilla para cita creada. "_Debes presentar tu credencial de identificación (INE) vigente_".
- Añadido _endpoint_ `exp_juzgados`. Para entrega de los juzgados de los que se pueden pedir expedientes, en el servicio de "revisión de expedientes" preferentemente para la unidad de "Archivo".
- Descripción de la versión en la documentación _swagger_ hecha por defecto.
- Archivo `README.md`. Más completo y organizado.
- Archivo `CONTRIBUTING.md`. Explica las reglas para colaborar en este proyecto.
- Archivo `.env.example` como ejemplo de la configuración de variables de entorno.


## [1.2.1] - 2026-05-20

### ✨ Mejoras

- Añadido campo de `código de asistencia` a la plantilla de email cita-creada.

### 🛠️ Cambios

- Cambio de asunto de correo de 'PJECZ' a 'SAJI'.
- Cambio en títulos plantillas de email.

### 🐞 Arreglado

- El _endpoint_ `mis_citas` ahora filtra que las citas no estén eliminadas y no sean pasadas a la fecha de hoy.


## [1.1.3] - 2026-04-26

### ✨ Mejoras

- Creación de plantillas para diferentes envíos de email, al crear, canelar citas y registro, cambio de contraseña de clientes.
- Uso de plantillas para envío de emails.
- Creación de servicio de envío de emails con plantillas.

### 🐞 Arreglado

- Locale, integración con el sistema operativo sobre el idioma de la fecha.