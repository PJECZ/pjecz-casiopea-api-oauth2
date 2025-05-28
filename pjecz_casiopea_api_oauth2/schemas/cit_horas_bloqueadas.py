"""
Cit Horas Bloqueadas v4, esquemas de pydantic
"""

from datetime import date, time

from pydantic import BaseModel, ConfigDict


class CitHoraBloqueadaOut(BaseModel):
    """Esquema para entregar horas bloqueadas"""

    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str
    fecha: date
    inicio: time
    termino: time
    descripcion: str
    model_config = ConfigDict(from_attributes=True)
