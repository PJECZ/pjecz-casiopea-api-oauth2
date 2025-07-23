"""
Distritos, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class DistritoOut(BaseModel):
    """Esquema para entregar distritos"""

    clave: str
    nombre: str
    nombre_corto: str
    es_distrito_judicial: bool
    es_distrito: bool
    es_jurisdiccional: bool
    model_config = ConfigDict(from_attributes=True)


class OneDistritoOut(BaseModel):
    """Esquema para entregar un distrito"""

    success: bool
    message: str
    data: DistritoOut | None = None
