"""
Cit Citas, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_uuid
from ..models.cit_citas import CitCita
from ..models.permisos import Permiso
from ..schemas.cit_citas import CitCitaOut, OneCitCitaOut
from ..schemas.cit_clientes import CitClienteInDB

cit_citas = APIRouter(prefix="/api/v5/cit_citas")


@cit_citas.get("/{cit_cita_id}", response_model=OneCitCitaOut)
async def detalle_cit_citas(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cita_id: str,
):
    """Detalle de una cita a partir de su ID, DEBE SER SUYA"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cita_id = safe_uuid(cit_cita_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la UUID")
    cit_cita = database.query(CitCita).get(cit_cita_id)
    if not cit_cita:
        return OneCitCitaOut(success=False, message="No existe esa cita")
    if cit_cita.estatus != "A":
        return OneCitCitaOut(success=False, message="No está habilitada esa cita")
    if cit_cita.cit_cliente_id != current_user.id:
        return OneCitCitaOut(success=False, message="No le pertenece esa cita")
    return OneCitCitaOut(success=True, message=f"Cita {cit_cita_id}", data=CitCitaOut.model_validate(cit_cita))


@cit_citas.get("", response_model=CustomPage[CitCitaOut])
async def paginado_cit_citas(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de SUS PROPIAS citas"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(CitCita).filter(CitCita.cit_cliente_id == current_user.id)
    return paginate(consulta.filter_by(estatus="A").order_by(CitCita.creado.desc()))
