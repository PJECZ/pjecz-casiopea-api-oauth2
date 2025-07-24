"""
Materias, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class MateriaOut(BaseModel):
    """Esquema para entregar materias"""

    clave: str
    nombre: str
    model_config = ConfigDict(from_attributes=True)


class OneMateriaOut(BaseModel):
    """Esquema para entregar una materia"""

    success: bool
    message: str
    data: MateriaOut | None = None
