"""
Cit Servicios, modelos
"""

import uuid
from datetime import time
from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class CitServicio(Base, UniversalMixin):
    """CitServicio"""

    # Nombre de la tabla
    __tablename__ = "cit_servicios"

    # Clave primaria
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Clave foránea
    cit_categoria_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cit_categorias.id"))
    cit_categoria: Mapped["CitCategoria"] = relationship(back_populates="cit_servicios")

    # Columnas
    clave: Mapped[str] = mapped_column(String(16), unique=True)
    descripcion: Mapped[str] = mapped_column(String(256))
    duracion: Mapped[time]
    documentos_limite: Mapped[int]
    desde: Mapped[Optional[time]]
    hasta: Mapped[Optional[time]]
    dias_habilitados: Mapped[str] = mapped_column(String(7))
    es_activo: Mapped[bool] = mapped_column(default=True)

    # Hijos
    cit_citas: Mapped[List["CitCita"]] = relationship("CitCita", back_populates="cit_servicio")
    cit_oficinas_servicios: Mapped[List["CitOficinaServicio"]] = relationship(
        "CitOficinaServicio", back_populates="cit_servicio"
    )

    @property
    def cit_categoria_clave(self):
        """Clave de la categoria"""
        return self.cit_categoria.clave

    @property
    def cit_categoria_nombre(self):
        """Nombre de la categoria"""
        return self.cit_categoria.nombre

    def __repr__(self):
        """Representación"""
        return f"<CitServicio {self.clave}>"
