"""
Cit Clientes Recuperaciones, esquemas de pydantic
"""

import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitClienteRecuperacionOut(BaseModel):
    """Esquema para entregar recuperaciones"""

    id: uuid.UUID
    relacion_id: str
    relacion_nombre: str
    fecha: date
    nombre: str
    descripcion: str
    archivo: str
    url: str
    model_config = ConfigDict(from_attributes=True)


class OneCitClienteRecuperacionOut(OneBaseOut):
    """Esquema para entregar una recuperación"""

    data: CitClienteRecuperacionOut | None = None
