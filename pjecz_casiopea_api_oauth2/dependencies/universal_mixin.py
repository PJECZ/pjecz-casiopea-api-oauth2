"""
UniversalMixin define las columnas y métodos comunes de todos los modelos
"""

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now
from sqlalchemy.types import CHAR


class UniversalMixin:
    """Columnas y métodos comunes a todas las tablas"""

    creado: Mapped[datetime] = mapped_column(default=now())
    modificado: Mapped[datetime] = mapped_column(default=now(), onupdate=now())
    estatus: Mapped[str] = mapped_column(CHAR, default="A")
