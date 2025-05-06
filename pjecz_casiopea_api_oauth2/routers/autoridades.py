"""
Autoridades, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.autoridades import Autoridad
from ..models.permisos import Permiso
from ..schemas.autoridades import AutoridadOut, OneAutoridadOut
from ..schemas.cit_clientes import CitClienteInDB

autoridades = APIRouter(prefix="/api/v5/autoridades")


@autoridades.get("/{clave}", response_model=OneAutoridadOut)
async def detalle_autoridades(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de una autoridad a partir de su clave"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        clave = safe_clave(clave)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        autoridad = database.query(Autoridad).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound) as error:
        return OneAutoridadOut(success=False, message="No existe esa autoridad")
    if autoridad.estatus != "A":
        message = "No está habilitada esa autoridad"
        return OneAutoridadOut(success=False, message=message)
    return OneAutoridadOut(success=True, message=f"Autoridad {clave}", data=AutoridadOut.model_validate(autoridad))


@autoridades.get("", response_model=CustomPage[AutoridadOut])
async def paginado_autoridades(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de autoridades"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(Autoridad).filter_by(estatus="A").order_by(Autoridad.clave))
