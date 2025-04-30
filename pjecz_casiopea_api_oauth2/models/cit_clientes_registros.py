"""
Cit Clientes Registros, modelos
"""

import uuid
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class CitClienteRegistro(Base, UniversalMixin):
    """CitClienteRegistro"""

    # Nombre de la tabla
    __tablename__ = "cit_clientes_registros"

    # Clave primaria
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Columnas
    nombres: Mapped[str] = mapped_column(String(256))
    apellido_primero: Mapped[str] = mapped_column(String(256))
    apellido_segundo: Mapped[str] = mapped_column(String(256))
    curp: Mapped[str] = mapped_column(String(18), index=True)
    telefono: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(256), index=True)
    expiracion: Mapped[datetime]
    cadena_validar: Mapped[str] = mapped_column(String(256))
    mensajes_cantidad: Mapped[int] = mapped_column(default=0)
    ya_registrado: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        """Representación"""
        return f"<CitClienteRegistro {self.id}>"
