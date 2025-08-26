"""
Cit Clientes, modelos
"""

import uuid
from datetime import date, datetime
from typing import List

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class CitCliente(Base, UniversalMixin):
    """CitCliente"""

    # Nombre de la tabla
    __tablename__ = "cit_clientes"

    # Clave primaria
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Columnas
    nombres: Mapped[str] = mapped_column(String(256))
    apellido_primero: Mapped[str] = mapped_column(String(256))
    apellido_segundo: Mapped[str] = mapped_column(String(256))
    curp: Mapped[str] = mapped_column(String(18), unique=True)
    telefono: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    contrasena_md5: Mapped[str] = mapped_column(String(256))
    contrasena_sha256: Mapped[str] = mapped_column(String(256))
    renovacion: Mapped[date]
    limite_citas_pendientes: Mapped[int] = mapped_column(default=3)

    # Columnas booleanas
    autoriza_mensajes: Mapped[bool] = mapped_column(default=True)
    enviar_boletin: Mapped[bool] = mapped_column(default=False)
    es_adulto_mayor: Mapped[bool] = mapped_column(default=False)
    es_mujer: Mapped[bool] = mapped_column(default=False)
    es_identidad: Mapped[bool] = mapped_column(default=False)
    es_discapacidad: Mapped[bool] = mapped_column(default=False)
    es_personal_interno: Mapped[bool] = mapped_column(default=False)

    # Hijos
    cit_citas: Mapped[List["CitCita"]] = relationship("CitCita", back_populates="cit_cliente")
    cit_clientes_recuperaciones: Mapped[List["CitClienteRecuperacion"]] = relationship(
        "CitClienteRecuperacion", back_populates="cit_cliente"
    )

    @property
    def nombre(self):
        """Junta nombres, apellido_primero y apellido segundo"""
        return self.nombres + " " + self.apellido_primero + " " + self.apellido_segundo

    @property
    def permissions(self):
        """Entrega un diccionario con todos los permisos si no ha llegado la fecha de renovación"""
        if self.renovacion < datetime.now().date():
            return {}
        # Los permisos son fijos para todos los clientes, donde 1 es solo lectura
        return {
            "AUTORIDADES": 1,
            "CIT CATEGORIAS": 1,
            "CIT CITAS": 3,
            "CIT RECUPERACIONES": 3,
            "CIT REGISTROS": 3,
            "CIT DIAS DISPONIBLES": 1,
            "CIT HORAS DISPONIBLES": 1,
            "CIT OFICINAS SERVICIOS": 1,
            "CIT SERVICIOS": 1,
            "DISTRITOS": 1,
            "DOMICILIOS": 1,
            "MATERIAS": 1,
            "OFICINAS": 1,
        }

    def __repr__(self):
        """Representación"""
        return f"<CitCliente {self.email}>"
