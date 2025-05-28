"""
Cit Días Inhábiles, routers
"""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..models.cit_dias_inhabiles import CitDiaInhabil
from ..models.permisos import Permiso
from ..schemas.cit_clientes import CitClienteInDB
from ..schemas.cit_dias_inhabiles import CitDiaInhabilOut, OneCitDiaInhabilOut

cit_dias_inhabiles = APIRouter(prefix="/api/v5/cit_dias_inhabiles")


@cit_dias_inhabiles.get("/{fecha}", response_model=OneCitDiaInhabilOut)
async def detalle(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    fecha: date,
):
    """Detalle de una día inhábil a partir de su clave"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_dia_inhabil = database.query(CitDiaInhabil).filter_by(fecha=fecha).one()
    except (MultipleResultsFound, NoResultFound):
        return OneCitDiaInhabilOut(success=False, message="No existe ese día inhábil")
    if cit_dia_inhabil.estatus != "A":
        return OneCitDiaInhabilOut(success=False, message="No está habilitado ese día inhábil")
    return OneCitDiaInhabilOut(
        success=True,
        message=f"Día inhábil {fecha}",
        data=CitDiaInhabilOut.model_validate(cit_dia_inhabil),
    )


@cit_dias_inhabiles.get("", response_model=CustomPage[CitDiaInhabilOut])
async def paginado(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    desde: date = None,
    hasta: date = None,
):
    """Paginado de días inhábiles"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(CitDiaInhabil)
    if desde is not None:
        consulta = consulta.filter(CitDiaInhabil.fecha >= desde)
    if hasta is not None:
        consulta = consulta.filter(CitDiaInhabil.fecha <= hasta)
    return paginate(consulta.filter_by(estatus="A").order_by(CitDiaInhabil.fecha.desc()))
