"""
Cit Clientes Registros, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.safe_string import safe_uuid
from ..models.cit_clientes_registros import CitClienteRegistro
from ..models.permisos import Permiso
from ..schemas.cit_clientes import CitClienteInDB
from ..schemas.cit_clientes_registros import CitClienteRegistroOut, OneCitClienteRegistroOut

cit_clientes_registros = APIRouter(prefix="/api/v5/cit_clientes_registros")


@cit_clientes_registros.get("/{cit_cliente_registro_id}", response_model=OneCitClienteRegistroOut)
async def detalle_cit_clientes_registros(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cliente_registro_id: str,
):
    """Detalle de una registro a partir de su ID"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente_registro_id = safe_uuid(cit_cliente_registro_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la UUID")
    cit_cliente_registro = database.query(CitClienteRegistro).get(cit_cliente_registro_id)
    if not cit_cliente_registro:
        return OneCitClienteRegistroOut(success=False, message="No existe ese registro")
    if cit_cliente_registro.estatus != "A":
        return OneCitClienteRegistroOut(success=False, message="No está habilitada esa registro")
    return OneCitClienteRegistroOut(
        success=True,
        message=f"Registro {cit_cliente_registro_id}",
        data=CitClienteRegistroOut.model_validate(cit_cliente_registro),
    )
