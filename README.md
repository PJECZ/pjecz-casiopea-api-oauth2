# 🏛️ [pjecz-casiopea-api-oauth2]

> API OAuth2 para dar servicio al proyecto _Frontend_ del sistema de citas SAJI.

Proyectos relaccionados:
- [pjecz-casiopea-api-key](https://github.com/PJECZ/pjecz-casiopea-api-key)
- [pjecz-casiopea-reactjs](https://github.com/PJECZ/pjecz-casiopea-reactjs)
- [pjecz-casiopea-flask](https://github.com/PJECZ/pjecz-casiopea-flask)

---

## 📋 Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Requisitos Previos](#requisitos-previos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Estructura de Ramas](#estructura-de-ramas)
- [Despliegue](#despliegue)
- [Contacto](#contacto)

---

## 📖 Descripción General
Es parte de un conjunto de proyecto para otorgar la comunicación vía por API's tipo OAuth2 al sistema _frontend_ que forma parte del **Sistema de citas SAJI** con cara al público. En este sistema hacemos la comunicación con base de datos y se aplican las reglas del negocio.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.14
* **Framework:** FastAPI
* **Base de Datos:** PostgreSQL
* **Servidor:** Nginx

## ⚙️ Requisitos Previos
Lista de herramientas necesarias para correr el proyecto localmente:
- Git
- Python
- uv - manejador de paquetes para Python

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio:
   ```bash
   git clone https://github.com/PJECZ/pjecz-casiopea-api-oauth2.git
   cd pjecz-casiopea-api-oauth2
   ```

### 2. Configurar variables de entorno:
Copia el archivo de ejemplo y edita las credenciales necesarias (Base de datos, API Keys):
```
cp .env.example .env
```

### 3. Instalar dependencias:
```bash
uv sync
```

### 4. Iniciar el servidor de desarrollo:
```bash
uv run flask run --host=0.0.0.0 --port=5022
```

## 🌿 Estructura de Ramas

Este proyecto sigue el flujo de trabajo institucional:
- `main`: Rama de producción (Solo código estable).
- `dev`: Rama de integración y pruebas (_staging_).
- `feature/*`: Ramas temporales para nuevas funcionalidades.

Ver más sobre como contribuir: [CONTRIBUTING](CONTRIBUTING.md)

## 🚢 Despliegue

Ejecutar comando en servidor de producción después de haber integrado el PR en la rama `dev`:

```bash
actualizar-proyecto-casiopea
```

---

## ✉️ Contacto

- **Departamento:** Dirección de Informática - PJECZ
- **Responsable:** Dir. Guillermo Valdés, Lucía Aranda y Ricardo Valdés
- **Email:** [correo@pjecz.gob.mx]

---

© 2026 Poder Judicial del Estado de Coahuila de Zaragoza.
