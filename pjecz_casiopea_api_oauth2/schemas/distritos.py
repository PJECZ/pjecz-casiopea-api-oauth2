"""
Distritos, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class DistritoOut(BaseModel):
    """Esquema para entregar distritos"""

    id: str
    clave: str
    nombre: str
    nombre_corto: str
    es_distrito_judicial: bool
    es_distrito: bool
    es_jurisdiccional: bool
    model_config = ConfigDict(from_attributes=True)


class OneDistritoOut(OneBaseOut):
    """Esquema para entregar un distrito"""

    data: DistritoOut | None = None
