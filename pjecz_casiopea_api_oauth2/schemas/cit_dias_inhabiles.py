"""
Cit Dias Inhábiles, esquemas de pydantic
"""

from datetime import date

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitDiaInhabilOut(BaseModel):
    """Esquema para entregar dias inhábiles"""

    id: str
    fecha: date
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OneCitDiaInhabilOut(OneBaseOut):
    """Esquema para entregar un día inhábil"""

    data: CitDiaInhabilOut | None = None
