"""
Cit Dias Inhábiles, esquemas de pydantic
"""

from datetime import date

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitDiaInhabilOut(BaseModel):
    """Esquema para entregar dias inhábiles"""

    fecha: date
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OneCitDiaInhabilOut(BaseModel):
    """Esquema para entregar un día inhábil"""

    success: bool
    message: str
    data: CitDiaInhabilOut | None = None
