"""
Authentications
"""

import re
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from ..models.cit_clientes import CitCliente
from ..schemas.cit_clientes import CitClienteInDB
from ..settings import Settings, get_settings
from .database import Session, get_db
from .exceptions import MyAnyError, MyAuthenticationError, MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from .safe_string import safe_email

ALGORITHM = "HS256"
PASSWORD_REGEXP = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,24}$"
TOKEN_EXPIRES_SECONDS = 3600  # 1 hora

# Autentificar con OAuth2 y solicitar token en @app.post("/token", response_model=Token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_cit_cliente_with_email(database: Session, email: str) -> CitClienteInDB:
    """Consultar un cliente por su email"""
    try:
        email = safe_email(email)
    except ValueError as error:
        raise MyNotValidParamError("El email no es válido") from error
    try:
        cit_cliente = database.query(CitCliente).filter(CitCliente.email == email).one()
    except (NoResultFound, MultipleResultsFound) as error:
        raise MyNotExistsError("No existe ese cliente") from error
    if cit_cliente.estatus != "A":
        raise MyIsDeletedError("No es activo ese cliente, está eliminado")
    datos = {
        "id": cit_cliente.id,
        "nombres": cit_cliente.nombres,
        "apellido_primero": cit_cliente.apellido_primero,
        "apellido_segundo": cit_cliente.apellido_segundo,
        "curp": cit_cliente.curp,
        "telefono": cit_cliente.telefono,
        "email": cit_cliente.email,
        "limite_citas_pendientes": cit_cliente.limite_citas_pendientes,
        "autoriza_mensajes": cit_cliente.autoriza_mensajes,
        "enviar_boletin": cit_cliente.enviar_boletin,
        "username": cit_cliente.email,
        "permissions": cit_cliente.permissions,
        "hashed_password": cit_cliente.contrasena_sha256,
        "disabled": cit_cliente.estatus != "A",
    }
    return CitClienteInDB(**datos)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Validar la contraseña"""
    if hashed_password == "":
        raise MyNotValidParamError("No tiene definida su contraseña")
    if re.match(PASSWORD_REGEXP, plain_password) is None:
        raise MyNotValidParamError("La contraseña no es valida")
    pwd_context = CryptContext(schemes=["pbkdf2_sha256", "des_crypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, database: Session = Depends(get_db)) -> CitClienteInDB:
    """Autentificar al cliente"""
    try:
        cit_cliente = get_cit_cliente_with_email(database, username)
    except MyAnyError as error:
        raise error
    if not verify_password(password, cit_cliente.hashed_password):
        raise MyAuthenticationError("La contraseña es incorrecta")
    return cit_cliente


def encode_token(settings: Settings, cit_cliente: CitClienteInDB) -> str:
    """Crear el token"""
    expiration_dt = datetime.now(timezone.utc) + timedelta(seconds=TOKEN_EXPIRES_SECONDS)
    expires_at = expiration_dt.timestamp()
    payload = {"username": cit_cliente.email, "expires_at": expires_at}
    return jwt.encode(payload=payload, key=settings.secret_key, algorithm=ALGORITHM)


def decode_token(token: str, settings: Settings) -> dict:
    """Decodificar el token"""
    try:
        payload = jwt.decode(jwt=token, key=settings.secret_key, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as error:
        raise MyAuthenticationError("No es válido el token") from error
    if "expires_at" not in payload or payload["expires_at"] < datetime.now(timezone.utc).timestamp():
        raise MyAuthenticationError("Ha caducado el token")
    return payload


async def get_current_active_user(
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> CitClienteInDB:
    """Obtener el cliente a partir del token"""
    try:
        decoded_token = decode_token(token, settings)
        cit_cliente = get_cit_cliente_with_email(database, decoded_token["username"])
    except MyAnyError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return cit_cliente
