"""
Cit Clientes Registros, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitClienteRegistroOut(BaseModel):
    """Esquema para entregar registros de clientes"""

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
