"""
Cit Clientes Registros, esquemas de pydantic
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitClienteRegistroOut(BaseModel):
    """Esquema para entregar registros de clientes"""

    id: uuid.UUID
    nombres: str
    apellido_primero: str
    apellido_segundo: str
    curp: str
    telefono: str
    email: str
    expiracion: datetime
    cadena_validar: str
    mensajes_cantidad: int
    ya_registrado: bool
    creado: datetime
    model_config = ConfigDict(from_attributes=True)


class OneCitClienteRegistroOut(OneBaseOut):
    """Esquema para entregar un registro de cliente"""

    data: CitClienteRegistroOut | None = None


class SolicitarCitClienteRegistroIn(BaseModel):
    """Esquema para recibir el registro de un cliente"""

    nombres: str
    apellido_primero: str
    apellido_segundo: str | None = None
    curp: str
    telefono: str
    email: str


class ValidarCitClienteRegistroIn(BaseModel):
    """Esquema para recibir la contraseña de un cliente"""

    id: uuid.UUID
    cadena_validar: str
    password: str


class TerminarCitClienteRegistroIn(ValidarCitClienteRegistroIn):
    """Esquema para recibir la contraseña de un cliente"""

    password: str
