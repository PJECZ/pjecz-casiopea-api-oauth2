# 🚀 Guía de Contribución

¡Gracias por querer mejorar este proyecto! Para mantener el código limpio y organizado, utilizamos un flujo de trabajo basado en **Forks** y dos ramas principales: `main` (producción) y `dev` (desarrollo).

## 🛠 Configuración Inicial

Antes de empezar, asegúrate de tener tu entorno listo:

1.  **Haz un Fork** de este repositorio a tu cuenta personal.
2.  **Clona tu Fork** localmente:
```bash
git clone https://github.com/PJECZ/pjecz-casiopea-api-oauth2.git
```
3.  **Configura el repositorio original** como `upstream` para recibir actualizaciones:
```bash
git remote add upstream https://github.com/PJECZ/pjecz-casiopea-api-oauth2.git
```

## 📈 Flujo de Trabajo (Git Flow)

### 1. Sincroniza tu rama `dev`

Antes de crear una nueva funcionalidad, asegúrate de tener lo último del proyecto principal:
```bash
# Cambia a la rama dev
git switch dev
# Baja cambios del proyecto principal y de tu rama dev
git pull upstream dev
```

### 2. Crea una rama para tu tarea

Usa nombres descriptivos como `feature/nombre-mejora` o `fix/bug-sesion`:
```Bash
git checkout -b feature/mi-nueva-mejora
```

### 3. Haz tus cambios y súbelos

Realiza tus _commits_ siguiendo el estándar de [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) si es posible.
Luego, sube la rama a **tu Fork**:

```bash
git push origin feature/mi-nueva-mejora
```

### 4. Abre un _Pull Request_ (PR)

Ve al repositorio original en GitHub y abre un PR:
- **Base:** `dev` (¡Importante! No envíes directamente a `main`).
- **Compare:** `tu-usuario:feature/mi-nueva-mejora`.

## 📋 Reglas de Oro

- **No toques `main`:** Solo el equipo de despliegue hace _merges_ de `dev` a `main`.
- **Tests:** Asegúrate de que tu código pasa todos los _tests_ locales antes de enviar el PR.
- **Documentación:** Si añades una funcionalidad nueva, actualiza el `README.md` de ser necesario y `CHANGELOG.md` para organizar los cambios añadidos.
- **Un PR por tarea:** No mezcles correcciones de errores con nuevas funcionalidades en el mismo PR.

## 🚀 Despliegue a Producción

Una vez que las funciones en `dev` son estables y han sido probadas, el administrador del proyecto realizará un _merge_ de `dev` hacia `main` para el despliegue final.

Revisando y añadiendo los cambios en el archivo `CHANGELOG.md`, subiendo la versión según sea el caso, borrar la rama `dev` después del _merge_ y crear una nueva rama `dev` cuando ya todo haya terminado.

```bash
git tag -a v1.0.0 -m "Lanzamiento versión 1.0"
git push origin v1.0.0
```
