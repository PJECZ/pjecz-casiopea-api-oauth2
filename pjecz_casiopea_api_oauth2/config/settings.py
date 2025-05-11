"""
Settings
"""

import os
from functools import lru_cache

from google.cloud import secretmanager
from pydantic_settings import BaseSettings

PROJECT_ID = os.getenv("PROJECT_ID", "")  # Por defecto está vacío, esto significa estamos en modo local
SERVICE_PREFIX = os.getenv("SERVICE_PREFIX", "pjecz_casiopea_api_oauth2")


def get_secret(secret_id: str) -> str:
    """Get secret from Google Cloud Secret Manager"""

    # If not in google cloud, return environment variable
    if PROJECT_ID == "":
        return os.getenv(secret_id.upper(), "")

    # Create the secret manager client
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    secret = f"{SERVICE_PREFIX}_{secret_id}"
    name = client.secret_version_path(PROJECT_ID, secret, "latest")

    # Access the secret version
    response = client.access_secret_version(name=name)

    # Return the decoded payload
    return response.payload.data.decode("UTF-8")


class Settings(BaseSettings):
    """Settings"""

    ACCESS_TOKEN_EXPIRE_MINUTES: int = get_secret("ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = os.getenv("ALGORITHM")
    DB_HOST: str = get_secret("db_host")
    DB_PORT: int = get_secret("db_port")
    DB_NAME: str = get_secret("db_name")
    DB_PASS: str = get_secret("db_pass")
    DB_USER: str = get_secret("db_user")
    ORIGINS: str = get_secret("origins")
    SECRET_KEY: str = get_secret("secret_key")
    TZ: str = get_secret("tz")

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
