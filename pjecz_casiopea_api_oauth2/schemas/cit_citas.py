"""
Cit Citas, esquemas de pydantic
"""

import uuid
from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitCitaCancelIn(BaseModel):
    """Esquema para cancelar una cita"""

    id: uuid.UUID
    cit_cliente_email: str


class CitCitaIn(BaseModel):
    """Esquema para crear una cita"""

    cit_servicio_clave: str
    fecha: date
    hora_minuto: time
    oficina_clave: str
    notas: str


class CitCitaOut(BaseModel):
    """Esquema para entregar citas"""

    id: uuid.UUID
    cit_cliente_nombre: str
    cit_servicio_clave: str
    cit_servicio_descripcion: str
    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str
    inicio: datetime
    termino: datetime
    notas: str
    estado: str
    asistencia: bool
    codigo_asistencia: str
    codigo_acceso_imagen_base64: str
    creado: datetime
    puede_cancelarse: bool
    model_config = ConfigDict(from_attributes=True)


class OneCitCitaOut(BaseModel):
    """Esquema para entregar un cita"""

    success: bool
    message: str
    data: CitCitaOut | None = None
