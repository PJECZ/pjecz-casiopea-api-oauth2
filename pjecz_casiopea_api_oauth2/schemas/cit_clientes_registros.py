"""
Cit Clientes Registros, esquemas de pydantic
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
    model_config = ConfigDict(from_attributes=True)


class OneCitClienteRegistroOut(BaseModel):
    """Esquema para entregar un registro de cliente"""

    success: bool
    message: str
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
    """Esquema para recibir la validación del e-mail del cliente"""

    id: str  # Es string porque debe ser receptor
    cadena_validar: str


class TerminarCitClienteRegistroIn(BaseModel):
    """Esquema para recibir la contraseña de un cliente"""

    id: str  # Es string porque debe ser receptor
    cadena_validar: str
    password: str
