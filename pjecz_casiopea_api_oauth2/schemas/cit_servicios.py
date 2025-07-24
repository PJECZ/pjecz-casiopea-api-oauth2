"""
Cit Servicios, esquemas de pydantic
"""

from datetime import time

from pydantic import BaseModel, ConfigDict


class CitServicioOut(BaseModel):
    """Esquema para entregar servicios"""

    cit_categoria_clave: str
    cit_categoria_nombre: str
    clave: str
    descripcion: str
    duracion: time
    documentos_limite: int
    desde: time
    hasta: time
    dias_habilitados: str
    model_config = ConfigDict(from_attributes=True)


class OneCitServicioOut(BaseModel):
    """Esquema para entregar un servicio"""

    success: bool
    message: str
    data: CitServicioOut | None = None
