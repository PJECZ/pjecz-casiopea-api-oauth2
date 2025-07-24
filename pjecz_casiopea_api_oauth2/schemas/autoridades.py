"""
Autoridades, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class AutoridadOut(BaseModel):
    """Esquema para entregar autoridades"""

    clave: str
    descripcion: str
    descripcion_corta: str
    distrito_clave: str
    distrito_nombre: str
    distrito_nombre_corto: str
    materia_clave: str
    materia_nombre: str
    es_jurisdiccional: bool
    model_config = ConfigDict(from_attributes=True)


class OneAutoridadOut(BaseModel):
    """Esquema para entregar un autoridad"""

    success: bool
    message: str
    data: AutoridadOut | None = None
