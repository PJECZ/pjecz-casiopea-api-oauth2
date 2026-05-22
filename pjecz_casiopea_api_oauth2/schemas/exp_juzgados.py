"""
Exp Juzgados, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class ExpJuzgadoOut(BaseModel):
    """Esquema para entregar exp-juzgados"""

    clave: str
    descripcion_corta: str
    descripcion: str
    model_config = ConfigDict(from_attributes=True)


class OneExpJuzgadoOut(BaseModel):
    """Esquema para entregar una exp-juzgados"""

    success: bool
    message: str
    data: ExpJuzgadoOut | None = None
