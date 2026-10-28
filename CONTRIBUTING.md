# 🚀 Guía de Contribución

¡Gracias por querer mejorar este proyecto! Para mantener el código limpio y organizado, utilizamos un flujo de trabajo basado en **Forks** y dos ramas principales: `main` (producción) y `dev` (desarrollo).

>[!info] Basado en plantilla v1.1.0 (2026-10-28)

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
4. Tu _remote_ personal (tu _fork_) debe llamarse **origin**.

## 📈 Flujo de Trabajo (GitFlow – Simplificado)

### 1. Sincroniza tu rama `dev`

Antes de crear una nueva funcionalidad, asegúrate de tener lo último del proyecto principal:
```bash
# Cambia a la rama dev
git switch dev
# Baja cambios del proyecto principal y de tu rama dev
git pull upstream dev
```

### 2. Crea una rama para tu tarea

Usa nombres descriptivos como `mejora/nombre-mejora` o `fix/bug-sesion`:
```Bash
git checkout -b mejora/mi-nueva-mejora
```

### 3. Haz tus cambios y súbelos

Realiza tus _commits_ siguiendo el estándar de [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) si es posible.
Luego, sube la rama a **tu Fork**:

```bash
git push origin mejora/mi-nueva-mejora
```

### 4. Abre un _Pull Request_ (PR)

Ve al repositorio original en GitHub y abre un PR:
- **Base:** `dev` (¡Importante! No envíes directamente a `main`).
- **Compare:** `tu-usuario:mejora/mi-nueva-mejora`.

## 📋 Reglas de Oro

- **No toques `main`:** Solo el equipo de despliegue hace _merges_ de `dev` a `main`.
- **Tests:** Asegúrate de que tu código pasa todos los _tests_ locales antes de enviar el PR.
- **Documentación:** Si añades una funcionalidad nueva, actualiza el `README.md` de ser necesario y `CHANGELOG.md` para organizar los cambios añadidos.
- **Un PR por tarea:** No mezcles correcciones de errores con nuevas funcionalidades en el mismo PR.

### 🌿Guía para nombres de ramas

Buenas prácticas para nombrar las ramas de trabajo.
Recuerda que desde tu _fork_ debes hacer una nueva rama basada en la rama de desarrollo `dev`.
Debes nombrar la rama según se explica más abajo, dependiendo de lo que vayas a hacer, por ejemplo una mejora en el _login_ del sitio, la rama basada en `dev` se deberá llamar: `mejora/login`, y en los _commits_ ir añadiendo buenos mensajes de descripción, ya explicados en el punto anterior.

| Abreviación                           | Descripción                                                                                          |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `feature/*`<br>`mejora/*`             | Nuevas funcionalidades o mejoras en algo.                                                            |
| `hotfix/*`                            | Arreglo crítico de algo, normalmente va directo a la rama `main` o de producción.                    |
| `bugfix/*`                            | Arreglo de un falló menor.                                                                           |
| `test/*`                              | Creación, modificación o mejora de un test.                                                          |
| `doc/*`                               | Creación, modificación o mejora en la documentación.                                                 |
| `refactor/*`                          | Código de mejora en legibilidad, funcionalidad o desempeño pero que no añade nuevas funcionalidades. |
| `desing/*`<br>`style/*`<br>`diseno/*` | Mejoras en la interfaz de usuario, páginas de presentación.                                          |

### 💬Guía para mensajes de _commit_

Buenas prácticas para mensajes de _commit_ entendibles.

| Abreviación | Descripción                                        |
| ----------- | -------------------------------------------------- |
| `feat:`     | Nueva función o mejora.                            |
| `fix:`      | Arreglo de un _bug_.                               |
| `docs:`     | Añadido o corregida la documentación del proyecto. |
| `style:`    | Cambios en el estilo, formato, etc.                |
| `refactor:` | Refactorización del código                         |
| `test:`     | Añadido o modificado algún _test_.                 |
| `chore:`    | Tarea de mantenimiento.                            |
| `perf:`     | Mejora en el rendimiento.                          |
| `ci:`       | Cambios relacionados al CI/CD.                     |

> [!TIP] Un buen mensaje de _commit_ es corto, claro y descriptivo.

## 🚀 Despliegue a Producción

Una vez que las funciones en `dev` son estables y han sido probadas, el administrador del proyecto realizará un _merge_ de `dev` hacia `main` para el despliegue final.

Revisando y añadiendo los cambios en el archivo `CHANGELOG.md`, subiendo la versión según sea el caso, borrar la rama `dev` después del _merge_ y crear una nueva rama `dev` cuando ya todo haya terminado.

```bash
git tag -a v1.0.0 -m "Lanzamiento versión 1.0"
git push origin v1.0.0
```

>[!Important] Para un _deploy_ en **GitHub** siga las instrucciones del documento: [DEPLOY](DEPLOY.md)

---

© 2026 Poder Judicial del Estado de Coahuila de Zaragoza.