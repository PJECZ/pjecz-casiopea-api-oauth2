"""
Cit Oficinas Servicios, routers
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.fastapi_pagination_custom_page import CustomPage
from ..dependencies.safe_string import safe_clave
from ..models.cit_oficinas_servicios import CitOficinaServicio
from ..models.cit_servicios import CitServicio
from ..models.oficinas import Oficina
from ..models.permisos import Permiso
from ..schemas.cit_clientes import CitClienteInDB
from ..schemas.cit_oficinas_servicios import CitOficinaServicioOut

cit_oficinas_servicios = APIRouter(prefix="/api/v5/cit_oficinas_servicios")


@cit_oficinas_servicios.get("", response_model=CustomPage[CitOficinaServicioOut])
async def paginado_cit_oficinas_servicios(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_servicio_clave: str = None,
    oficina_clave: str = None,
):
    """Paginado de oficinas-servicios"""
    if current_user.permissions.get("CIT OFICINAS SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    consulta = database.query(CitOficinaServicio)
    if cit_servicio_clave is not None:
        try:
            cit_servicio_clave = safe_clave(cit_servicio_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave de la oficina")
        consulta = consulta.join(CitServicio).filter(CitServicio.clave == cit_servicio_clave)
    if oficina_clave is not None:
        try:
            oficina_clave = safe_clave(oficina_clave)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es válida la clave de la oficina")
        consulta = consulta.join(Oficina).filter(Oficina.clave == oficina_clave)
    return paginate(consulta.filter_by(estatus="A").order_by(CitOficinaServicio.creado.desc()))
