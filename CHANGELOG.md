# 📝 Historial de Cambios (Changelog)

Todos los cambios notables en este proyecto serán documentados en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).


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