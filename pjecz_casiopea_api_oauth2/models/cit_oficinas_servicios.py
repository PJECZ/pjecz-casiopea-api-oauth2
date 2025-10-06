"""
Cit Oficinas Servicios, modelos
"""

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class CitOficinaServicio(Base, UniversalMixin):
    """CitOficinaServicio"""

    # Nombre de la tabla
    __tablename__ = "cit_oficinas_servicios"

    # Clave primaria
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Claves foráneas
    cit_servicio_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cit_servicios.id"))
    cit_servicio: Mapped["CitServicio"] = relationship(back_populates="cit_oficinas_servicios")
    oficina_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("oficinas.id"))
    oficina: Mapped["Oficina"] = relationship(back_populates="cit_oficinas_servicios")

    # Columnas
    descripcion: Mapped[str] = mapped_column(String(256))
    es_activo: Mapped[bool] = mapped_column(default=True)

    @property
    def cit_servicio_clave(self):
        """Clave del servicio"""
        return self.cit_servicio.clave

    @property
    def cit_servicio_descripcion(self):
        """Descripcion del servicio"""
        return self.cit_servicio.descripcion

    @property
    def oficina_clave(self):
        """Clave de la oficina"""
        return self.oficina.clave

    @property
    def oficina_descripcion(self):
        """Descripcion de la oficina"""
        return self.oficina.descripcion

    @property
    def oficina_descripcion_corta(self):
        """Descripcion corta de la oficina"""
        return self.oficina.descripcion_corta

    def __repr__(self):
        """Representación"""
        return f"<CitOficinaServicio {self.id}>"
