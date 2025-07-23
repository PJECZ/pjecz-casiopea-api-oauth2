"""
Cit Categorías, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class CitCategoriaOut(BaseModel):
    """Esquema para entregar categorías"""

    clave: str
    nombre: str
    model_config = ConfigDict(from_attributes=True)


class OneCitCategoriaOut(BaseModel):
    """Esquema para entregar una categoría"""

    success: bool
    message: str
    data: CitCategoriaOut | None = None
