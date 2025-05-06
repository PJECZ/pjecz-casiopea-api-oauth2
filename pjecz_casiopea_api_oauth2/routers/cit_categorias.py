"""
Cit Categorías, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.cit_categorias import CitCategoria
from ..models.permisos import Permiso
from ..schemas.cit_categorias import CitCategoriaOut, OneCitCategoriaOut
from ..schemas.cit_clientes import CitClienteInDB

cit_categorias = APIRouter(prefix="/api/v5/cit_categorias")


@cit_categorias.get("/{clave}", response_model=OneCitCategoriaOut)
async def detalle_cit_categorias(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de una categoria a partir de su clave"""
    if current_user.permissions.get("CIT CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        clave = safe_clave(clave)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave")
    try:
        cit_categoria = database.query(CitCategoria).filter_by(clave=clave).one()
    except (MultipleResultsFound, NoResultFound) as error:
        return OneCitCategoriaOut(success=False, message="No existe esa categoria")
    if cit_categoria.estatus != "A":
        return OneCitCategoriaOut(success=False, message="No está habilitada esa categoria")
    return OneCitCategoriaOut(
        success=True,
        message=f"Categoría {clave}",
        data=CitCategoriaOut.model_validate(cit_categoria),
    )


@cit_categorias.get("", response_model=CustomPage[CitCategoriaOut])
async def paginado_cit_categorias(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de categorías"""
    if current_user.permissions.get("CIT CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(database.query(CitCategoria).filter_by(estatus="A").order_by(CitCategoria.nombre))
