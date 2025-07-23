"""
Domicilios, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class DomicilioOut(BaseModel):
    """Esquema para entregar domicilios"""

    clave: str
    edificio: str
    estado: str
    municipio: str
    calle: str
    num_ext: str
    num_int: str
    colonia: str
    cp: int
    completo: str
    model_config = ConfigDict(from_attributes=True)


class OneDomicilioOut(BaseModel):
    """Esquema para entregar un domicilio"""

    success: bool
    message: str
    data: DomicilioOut | None = None
