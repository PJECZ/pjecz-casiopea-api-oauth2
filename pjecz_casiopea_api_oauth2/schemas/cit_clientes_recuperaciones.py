"""
Cit Clientes Recuperaciones, esquemas de pydantic
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CitClienteRecuperacionOut(BaseModel):
    """Esquema para entregar recuperaciones"""

    id: uuid.UUID
    expiracion: datetime
    model_config = ConfigDict(from_attributes=True)


class OneCitClienteRecuperacionOut(BaseModel):
    """Esquema para entregar una recuperación"""

    success: bool
    message: str
    data: CitClienteRecuperacionOut | None = None


class SolicitarCitClienteRecuperacionIn(BaseModel):
    """Esquema para recibir una recuperación"""

    email: str


class ValidarCitClienteRecuperacionIn(BaseModel):
    """Esquema para recibir la validación de la recuperación"""

    id: str  # Es string porque debe ser receptor
    cadena_validar: str


class TerminarCitClienteRecuperacionIn(BaseModel):
    """Esquema para recibir la contraseña desde la recuperación"""

    id: str  # Es string porque debe ser receptor
    cadena_validar: str
    password: str
