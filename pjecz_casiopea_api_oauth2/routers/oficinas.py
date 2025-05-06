"""
Oficinas, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.oficinas import Oficina
from ..models.permisos import Permiso
from ..schemas.cit_clientes import CitClienteInDB
from ..schemas.oficinas import OficinaOut, OneOficinaOut

oficinas = APIRouter(prefix="/api/v5/oficinas")


@oficinas.get("/{clave}", response_model=OneOficinaOut)
async def detalle_oficinas(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de una oficina a partir de su clave"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        clave = safe_clave(clave)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        oficina = database.query(Oficina).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound) as error:
        return OneOficinaOut(success=False, message="No existe esa oficina")
    if oficina.estatus != "A":
        return OneOficinaOut(success=False, message="No está habilitada esa oficina")
    return OneOficinaOut(success=True, message=f"Detalle de {clave}", data=OficinaOut.model_validate(oficina))


@oficinas.get("", response_model=CustomPage[OficinaOut])
async def paginado_oficinas(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de oficinas"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(Oficina).filter_by(estatus="A").order_by(Oficina.clave))
