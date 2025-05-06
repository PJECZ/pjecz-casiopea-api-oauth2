"""
Cit Clientes, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies.authentications import get_current_active_user
from ..dependencies.safe_string import safe_email
from ..models.permisos import Permiso
from ..schemas.cit_clientes import CitClienteInDB, CitClienteOut, OneCitClienteOut

cit_clientes = APIRouter(prefix="/api/v5/cit_clientes")


@cit_clientes.get("/{email}", response_model=OneCitClienteOut)
async def detalle_cit_clientes(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    email: str,
):
    """Detalle de SU PROPIO cliente a partir de su email, no tiene capacidad de consultar otros clientes"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        email = safe_email(email)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válido el email")
    if current_user.email != email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No es su e-mail")
    data = CitClienteOut(
        id=current_user.id,
        nombres=current_user.nombres,
        apellido_primero=current_user.apellido_primero,
        apellido_segundo=current_user.apellido_segundo,
        curp=current_user.curp,
        telefono=current_user.telefono,
        email=email,
        limite_citas_pendientes=current_user.limite_citas_pendientes,
        autoriza_mensajes=current_user.autoriza_mensajes,
        enviar_boletin=current_user.enviar_boletin,
    )
    return OneCitClienteOut(success=True, message=f"Cliente {email}", data=data)
