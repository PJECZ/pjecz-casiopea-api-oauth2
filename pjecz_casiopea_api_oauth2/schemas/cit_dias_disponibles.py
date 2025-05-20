"""
Cit Días Disponibles, esquemas de pydantic
"""

from datetime import date

from pydantic import BaseModel


class ListCitDiaDisponibleOut(BaseModel):
    """Esquema para entregar el listado de días disponibles"""

    success: bool
    message: str
    data: list[date] | None = None
