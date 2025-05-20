"""
Cit Clientes Recuperaciones, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave, safe_uuid
from ..models.cit_clientes_recuperaciones import CitClienteRecuperacion
from ..models.permisos import Permiso
from ..schemas.cit_clientes import CitClienteInDB
from ..schemas.cit_clientes_recuperaciones import CitClienteRecuperacionOut, OneCitClienteRecuperacionOut

cit_clientes_recuperaciones = APIRouter(prefix="/api/v5/cit_clientes_recuperaciones")


@cit_clientes_recuperaciones.get("/{cit_cliente_recuperacion_id}", response_model=OneCitClienteRecuperacionOut)
async def detalle_cit_clientes_recuperaciones(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cliente_recuperacion_id: str,
):
    """Detalle de una recuperación a partir de su ID, DEBE SER SUYA"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente_recuperacion_id = safe_uuid(cit_cliente_recuperacion_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la UUID")
    cit_cliente_recuperacion = database.query(CitClienteRecuperacion).get(cit_cliente_recuperacion_id)
    if not cit_cliente_recuperacion:
        return OneCitClienteRecuperacionOut(success=False, message="No existe esa recuperación")
    if cit_cliente_recuperacion.estatus != "A":
        return OneCitClienteRecuperacionOut(success=False, message="No está habilitada esa recuperacion")
    if cit_cliente_recuperacion.cit_cliente_id != current_user.id:
        return OneCitClienteRecuperacionOut(success=False, message="No le pertenece esa recuperación")
    return OneCitClienteRecuperacionOut(
        success=True,
        message=f"Recuperación {cit_cliente_recuperacion_id}",
        data=CitClienteRecuperacionOut.model_validate(cit_cliente_recuperacion),
    )


@cit_clientes_recuperaciones.get("", response_model=CustomPage[CitClienteRecuperacionOut])
async def paginado_cit_clientes_recuperaciones(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de SUS PROPIAS recuperaciones"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(CitClienteRecuperacion).filter(CitClienteRecuperacion.cit_cliente_id == current_user.id)
    return paginate(consulta.filter_by(estatus="A").order_by(CitClienteRecuperacion.creado.desc()))
