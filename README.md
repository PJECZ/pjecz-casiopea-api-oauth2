# 🏛️ pjecz-casiopea-api-oauth2

> API OAuth2 para dar servicio al proyecto _Frontend_ del sistema de citas SAJI.

>[!info] Basado en plantilla v1.1.0 (2026-10-28)

## 🗃️ Proyectos relacionados:

- [pjecz-casiopea-api-key](https://github.com/PJECZ/pjecz-casiopea-api-key)
- [pjecz-casiopea-reactjs](https://github.com/PJECZ/pjecz-casiopea-reactjs)
- [pjecz-casiopea-flask](https://github.com/PJECZ/pjecz-casiopea-flask)

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

## 🧩 IDE y sus extensiones recomendadas

Como IDE para este proyecto se recomienda **VS Code** y para mayor complemento se pueden instalar las siguientes extensiones:

- **Material Icon Theme** ~ _Philipp Kief_ – Mejora los iconos en el árbol de archivos.
- **Git Graph** ~ *mhutchie* – Muestra de manera gráfica el historial Git del proyecto.
- **GitHub Pull Request** ~ *GitHub* – Permite hacer Pull Request desde VSCode.
- **indent-rainbow** ~ *oderwat* – Da apoyo visual a las identaciones en el código.
- **WSL** ~ *Microsoft* – Para abrir e editar proyectos dentro del directorio WSL de Windos.

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
- `mejora/*`: Ramas temporales para nuevas funcionalidades.

Ver más sobre como contribuir: [CONTRIBUTING](CONTRIBUTING.md)

## 📝 Documentar cambios

Archivo que almacena los cambios efectuados en el proyecto, su propósito es informar a los usuarios y desarrolladores qué ha cambiado exactamente entre versiones.

**Definición Oficial**: Un registro de cambios, «changelog» de ahora en adelante, es un archivo que contiene una lista cronológicamente ordenada de los cambios más destacables para cada versión de un proyecto.

Recuerde que con cada entrega debe añadir la mejora, arreglo, modificación o eliminación hecha por ese _commit_. Como recomendación, dejé abierto este documento siempre que trabaje en el proyecto y vaya indicado los cambios que hace. Cuando haga un _deploy_ añada la fecha de entrega a la última versión en la que se trabajó.

Lleve ese registro en el archivo: [CHANGELOG](CHANGELOG.md)

## 🚚 Deploy

Instrucciones de cómo hacer un deploy si sigue el flujo de trabajo **GitFlow - Simplificado** y su proyecto está alojado en **GitHub**. Véase: [DEPLOY](DEPLOY.md)

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
