"""
Autoridades, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class AutoridadOut(BaseModel):
    """Esquema para entregar autoridades"""

    id: str
    distrito_id: str
    distrito_clave: str
    distrito_nombre: str
    distrito_nombre_corto: str
    materia_id: str
    materia_clave: str
    materia_nombre: str
    clave: str
    descripcion: str
    descripcion_corta: str
    es_jurisdiccional: bool
    es_notaria: bool
    es_organo_especializado: bool
    organo_jurisdiccional: str
    audiencia_categoria: str
    model_config = ConfigDict(from_attributes=True)


class OneAutoridadOut(OneBaseOut):
    """Esquema para entregar un autoridad"""

    data: AutoridadOut | None = None
