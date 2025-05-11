"""
Materias, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ..dependencies.schemas_base import OneBaseOut


class MateriaOut(BaseModel):
    """Esquema para entregar materias"""

    clave: str
    nombre: str
    model_config = ConfigDict(from_attributes=True)


class OneMateriaOut(OneBaseOut):
    """Esquema para entregar una materia"""

    data: MateriaOut | None = None
