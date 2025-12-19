# pjecz-casiopea-api-oauth2

API con autentificación OAuth2 del sistema de citas

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:

```env
# Base de datos
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=pjecz_casiopea
DB_USER=adminpjeczcasiopea
DB_PASS=XXXXXXXXXXXXXXXX

# Origins
ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# OAuth2
ACCESS_TOKEN_EXPIRE_SECONDS=3600
ALGORITHM=HS256
SECRET_KEY=

# Huso Horario
TZ=America/Mexico_City

# Control de Acceso API Key para obtener el código de acceso
CONTROL_ACCESO_URL=
CONTROL_ACCESO_API_KEY=
CONTROL_ACCESO_APLICACION=
CONTROL_ACCESO_TIMEOUT=

# SendGrid para enviar correos electrónicos
HOST=http://localhost:3000
NEW_ACCOUNT_WEB_PAGE_URL=
RECOVER_WEB_PAGE_URL=
SENDGRID_API_KEY=
SENDGRID_FROM_EMAIL=
```
