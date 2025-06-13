"""
Domicilios, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.domicilios import Domicilio
from ..models.permisos import Permiso
from ..schemas.cit_clientes import CitClienteInDB
from ..schemas.domicilios import DomicilioOut, OneDomicilioOut

domicilios = APIRouter(prefix="/api/v5/domicilios")


@domicilios.get("/{clave}", response_model=OneDomicilioOut)
async def detalle(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de un domicilio a partir de su ID"""
    if current_user.permissions.get("DOMICILIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        clave = safe_clave(clave)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        domicilio = database.query(Domicilio).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound):
        return OneDomicilioOut(success=False, message="No existe ese domicilio")
    if domicilio.es_activo is False:
        return OneDomicilioOut(success=False, message="No está activo ese domicilio")
    if domicilio.estatus != "A":
        return OneDomicilioOut(success=False, message="Este domicilio está eliminado")
    return OneDomicilioOut(success=True, message=f"Detalle de {clave}", data=DomicilioOut.model_validate(domicilio))


@domicilios.get("", response_model=CustomPage[DomicilioOut])
async def paginado(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de domicilios"""
    if current_user.permissions.get("DOMICILIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(Domicilio).filter_by(es_activo=True).filter_by(estatus="A").order_by(Domicilio.edificio))
