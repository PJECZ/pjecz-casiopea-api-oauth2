"""
Cit Citas, esquemas de pydantic
"""

from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitCitaCancelIn(BaseModel):
    """Esquema para cancelar una cita"""

    id: str
    cit_cliente_id: str


class CitCitaIn(BaseModel):
    """Esquema para crear una cita"""

    cit_cliente_id: str
    cit_servicio_id: str
    fecha: date
    hora_minuto: time
    oficina_id: str
    notas: str


class CitCitaOut(BaseModel):
    """Esquema para entregar citas"""

    id: str
    cit_cliente_id: str
    cit_cliente_nombre: str
    cit_cliente_curp: str
    cit_cliente_email: str
    cit_servicio_id: str
    cit_servicio_clave: str
    cit_servicio_descripcion: str
    oficina_id: str
    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str
    inicio: datetime
    termino: datetime
    notas: str
    estado: str
    asistencia: bool
    codigo_asistencia: str
    creado: datetime
    puede_cancelarse: bool
    model_config = ConfigDict(from_attributes=True)


class OneCitCitaOut(OneBaseOut):
    """Esquema para entregar un cita"""

    data: CitCitaOut | None = None
