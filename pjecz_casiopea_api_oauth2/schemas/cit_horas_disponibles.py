"""
Cit Horas Disponibles, esquemas de pydantic
"""

from datetime import time

from pydantic import BaseModel


class ListCitHoraDisponibleOut(BaseModel):
    """Esquema para entregar el listado de horas disponibles"""

    success: bool
    message: str
    data: list[time] | None = None
