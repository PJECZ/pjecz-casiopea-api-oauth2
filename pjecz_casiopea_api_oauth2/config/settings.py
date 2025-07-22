"""
Settings
"""

import os
from functools import lru_cache

import google.auth
from google.cloud import secretmanager
from pydantic_settings import BaseSettings

# PROJECT_ID = os.getenv("PROJECT_ID", "")  # Por defecto está vacío, esto significa estamos en modo local
SERVICE_PREFIX = os.getenv("SERVICE_PREFIX", "pjecz_casiopea_api_oauth2")


def get_secret(secret_id: str, default: str = "") -> str:
    """Get secret from Google Cloud Secret Manager"""

    # Obtener el project_id con la librería de Google Auth
    _, project_id = google.auth.default()

    # Si NO estamos en Google Cloud, entonces se está ejecutando de forma local
    if not project_id:
        # Entregar el valor de la variable de entorno, si no esta definida, se entrega el valor por defecto
        value = os.getenv(secret_id.upper())
        if value is None:
            return default
        return value

    # Tratar de obtener el secreto
    try:
        # Create the secret manager client
        client = secretmanager.SecretManagerServiceClient()
        # Build the resource name of the secret version
        secret = f"{SERVICE_PREFIX}_{secret_id}"
        name = client.secret_version_path(project_id, secret, "latest")
        # Access the secret version
        response = client.access_secret_version(name=name)
        # Return the decoded payload
        return response.payload.data.decode("UTF-8")
    except:
        pass

    # Entregar el valor por defecto porque no existe el secreto, ni la variable de entorno
    return default


class Settings(BaseSettings):
    """Settings"""

    ACCESS_TOKEN_EXPIRE_SECONDS: int = int(get_secret("ACCESS_TOKEN_EXPIRE_SECONDS", "3600"))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    CONTROL_ACCESO_URL: str = os.getenv("CONTROL_ACCESO_URL", "")
    CONTROL_ACCESO_API_KEY: str = os.getenv("CONTROL_ACCESO_API_KEY", "")
    CONTROL_ACCESO_APLICACION: int = int(os.getenv("CONTROL_ACCESO_APLICACION", ""))
    CONTROL_ACCESO_TIMEOUT: int = int(os.getenv("CONTROL_ACCESO_TIMEOUT", "60"))
    DB_HOST: str = get_secret("DB_HOST")
    DB_PORT: int = int(get_secret("DB_PORT", "5432"))
    DB_NAME: str = get_secret("DB_NAME")
    DB_PASS: str = get_secret("DB_PASS")
    DB_USER: str = get_secret("DB_USER")
    ORIGINS: str = get_secret("ORIGINS")
    REDIS_URL: str = get_secret("REDIS_URL", "redis://localhost:6379/0")
    TASK_QUEUE: str = get_secret("TASK_QUEUE", "pjecz_casiopea")
    SECRET_KEY: str = get_secret("SECRET_KEY")
    SENDGRID_API_KEY: str = get_secret("SENDGRID_API_KEY")
    SENDGRID_FROM_EMAIL: str = get_secret("SENDGRID_FROM_EMAIL")
    TZ: str = get_secret("TZ")

    class Config:
        """Load configuration"""

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Customise sources, first environment variables, then .env file, then google cloud secret manager"""
            return env_settings, file_secret_settings, init_settings


@lru_cache()
def get_settings() -> Settings:
    """Get Settings"""
    return Settings()
