"""
Cit Clientes, esquemas de pydantic
"""

import uuid

from pydantic import BaseModel, ConfigDict


class CitClienteOut(BaseModel):
    """Esquema para entregar clientes"""

    nombres: str
    apellido_primero: str
    apellido_segundo: str
    curp: str
    telefono: str
    email: str
    limite_citas_pendientes: int
    autoriza_mensajes: bool
    enviar_boletin: bool
    model_config = ConfigDict(from_attributes=True)


class CitClienteInDB(CitClienteOut):
    """Cliente en base de datos"""

    id: uuid.UUID
    username: str
    permissions: dict
    hashed_password: str
    disabled: bool


class OneCitClienteOut(BaseModel):
    """Esquema para entregar un cliente"""

    success: bool
    message: str
    data: CitClienteOut | None = None


class Token(BaseModel):
    """Token"""

    access_token: str
    expires_in: int
    token_type: str
    username: str


class TokenData(BaseModel):
    """Token data"""

    username: str


class CitClienteActualizarContrasenaIn(BaseModel):
    """Esquema para recibir la actualización de la contraseña"""

    email: str
    contrasena_anterior: str
    contrasena_nueva: str


class CitClienteActualizarContrasenaOut(CitClienteOut):
    """Esquema para entregar los datos del cliente y el mensaje de la actualización de la contraseña"""

    mensaje: str
