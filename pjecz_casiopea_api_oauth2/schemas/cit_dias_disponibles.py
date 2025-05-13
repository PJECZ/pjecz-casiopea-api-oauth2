"""
Cit Días Disponibles, esquemas de pydantic
"""

from pydantic import BaseModel


class ListCitDiaDisponibleOut(BaseModel):
    """Esquema para entregar el listado de días disponibles"""

    success: bool
    message: str
    data: list | None = None
