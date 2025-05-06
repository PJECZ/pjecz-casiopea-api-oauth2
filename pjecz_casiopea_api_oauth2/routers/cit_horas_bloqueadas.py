"""
Cit Horas Bloqueadas, routers
"""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave, safe_uuid
from ..models.cit_horas_bloqueadas import CitHoraBloqueada
from ..models.oficinas import Oficina
from ..models.permisos import Permiso
from ..schemas.cit_clientes import CitClienteInDB
from ..schemas.cit_horas_bloqueadas import CitHoraBloqueadaOut, OneCitHoraBloqueadaOut

cit_horas_bloqueadas = APIRouter(prefix="/api/v5/cit_horas_bloqueadas")


@cit_horas_bloqueadas.get("/{cit_hora_bloqueada_id}", response_model=OneCitHoraBloqueadaOut)
async def detalle_cit_horas_bloqueadas(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_hora_bloqueada_id: str,
):
    """Detalle de una hora bloqueada a partir de su ID"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_hora_bloqueada_id = safe_uuid(cit_hora_bloqueada_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la UUID")
    cit_hora_bloqueada = database.query(CitHoraBloqueada).get(cit_hora_bloqueada_id)
    if not cit_hora_bloqueada:
        return OneCitHoraBloqueadaOut(success=False, message="No existe esa hora bloqueada")
    if cit_hora_bloqueada.estatus != "A":
        return OneCitHoraBloqueadaOut(success=False, message="No está habilitada esa hora bloqueada")
    return OneCitHoraBloqueadaOut(
        success=True,
        message=f"Hora bloqueada {cit_hora_bloqueada_id}",
        data=CitHoraBloqueadaOut.model_validate(cit_horas_bloqueadas),
    )


@cit_horas_bloqueadas.get("", response_model=CustomPage[CitHoraBloqueadaOut])
async def paginado_cit_horas_bloqueadas(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    fecha: date,
    oficina_clave: str,
):
    """Paginado de horas bloqueadas"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(CitHoraBloqueada)
    if fecha is not None:
        consulta = consulta.filter(CitHoraBloqueada.fecha == fecha)
    if oficina_clave is not None:
        try:
            oficina_clave = safe_clave(oficina_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave de la oficina")
        consulta = consulta.join(Oficina).filter(Oficina.clave == oficina_clave)
    return paginate(consulta.filter_by(estatus="A").order_by(CitHoraBloqueada.creado.desc()))
