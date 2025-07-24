"""
Oficinas, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class OficinaOut(BaseModel):
    """Esquema para entregar oficinas"""

    clave: str
    descripcion: str
    descripcion_corta: str
    domicilio_clave: str
    domicilio_completo: str
    domicilio_edificio: str
    es_jurisdiccional: bool
    model_config = ConfigDict(from_attributes=True)


class OneOficinaOut(BaseModel):
    """Esquema para entregar una oficina"""

    success: bool
    message: str
    data: OficinaOut | None = None
