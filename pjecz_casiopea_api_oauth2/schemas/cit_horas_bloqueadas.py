"""
Cit Horas Bloqueadas v4, esquemas de pydantic
"""

from datetime import date, time

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitHoraBloqueadaOut(BaseModel):
    """Esquema para entregar horas bloqueadas"""

    id: str
    oficina_id: str
    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str
    fecha: date
    inicio: time
    termino: time
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OneCitHoraBloqueadaOut(OneBaseOut):
    """Esquema para entregar un hora bloqueada"""

    data: CitHoraBloqueadaOut | None = None
