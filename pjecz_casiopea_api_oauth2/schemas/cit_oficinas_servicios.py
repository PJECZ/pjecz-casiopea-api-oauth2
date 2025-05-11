"""
Cit Oficinas Servicios, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitOficinaServicioOut(BaseModel):
    """Esquema para entregar oficinas-servicios"""

    cit_servicio_clave: str
    cit_servicio_descripcion: str
    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str
    model_config = ConfigDict(from_attributes=True)


class OneCitOficinaServicioOut(OneBaseOut):
    """Esquema para entregar un oficina-servicio"""

    data: CitOficinaServicioOut | None = None
