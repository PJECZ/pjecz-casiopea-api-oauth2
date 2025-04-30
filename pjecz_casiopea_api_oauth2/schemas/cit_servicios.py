"""
Cit Servicios, esquemas de pydantic
"""

from datetime import time

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitServicioOut(BaseModel):
    """Esquema para entregar servicios"""

    id: str
    cit_categoria_id: str
    cit_categoria_nombre: str
    clave: str
    descripcion: str
    duracion: time
    documentos_limite: int
    desde: time
    hasta: time
    dias_habilitados: str
    model_config = ConfigDict(from_attributes=True)


class OneCitServicioOut(OneBaseOut):
    """Esquema para entregar un servicio"""

    data: CitServicioOut | None = None
