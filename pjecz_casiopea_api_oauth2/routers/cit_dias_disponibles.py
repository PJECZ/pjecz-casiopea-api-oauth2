"""
Cit Días Disponibles, routers
"""

from datetime import date, datetime, timedelta
from typing import Annotated

import pytz
from fastapi import APIRouter, Depends, HTTPException, status

from ..config.settings import Settings, get_settings
from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..models.cit_dias_inhabiles import CitDiaInhabil
from ..models.permisos import Permiso
from ..schemas.cit_clientes import CitClienteInDB
from ..schemas.cit_dias_disponibles import ListCitDiaDisponibleOut

LIMITE_DIAS = 90
QUITAR_PRIMER_DIA_DESPUES_HORAS = 14

cit_dias_disponibles = APIRouter(prefix="/api/v5/cit_dias_disponibles")


def listar_dias_disponibles(
    database: Session,
    settings: Settings,
) -> list[date]:
    """Listar los días disponibles"""

    # Consultar los días inhábiles
    cit_dias_inhabiles = (
        database.query(CitDiaInhabil)
        .filter(CitDiaInhabil.fecha >= date.today())
        .filter(CitDiaInhabil.estatus == "A")
        .order_by(CitDiaInhabil.fecha)
        .all()
    )
    dias_inhabiles = [item.fecha for item in cit_dias_inhabiles]

    # Acumular los días
    dias_disponibles = []
    for fecha in (date.today() + timedelta(n) for n in range(1, LIMITE_DIAS)):
        if fecha.weekday() in (5, 6):  # Quitar los sábados y domingos
            continue
        if fecha in dias_inhabiles:  # Quitar los dias inhábiles
            continue
        dias_disponibles.append(fecha)  # Acumular

    # Determinar el dia de hoy
    servidor_tz = pytz.UTC
    local_tz = pytz.timezone(settings.TZ)
    servidor_ts = datetime.now(tz=servidor_tz)
    local_ts = servidor_ts.astimezone(local_tz)
    hoy = local_ts.date()

    # Si hoy es sábado, domingo o dia inhábil, quitar el primer día disponible
    hoy_es_sabado_o_domingo = hoy.weekday() in (5, 6)
    hoy_es_dia_inhabil = hoy in dias_inhabiles
    pasa_de_la_hora = local_ts.hour > QUITAR_PRIMER_DIA_DESPUES_HORAS
    if hoy_es_sabado_o_domingo or hoy_es_dia_inhabil or pasa_de_la_hora:
        dias_disponibles.pop(0)

    # Entregar
    return dias_disponibles


@cit_dias_disponibles.get("", response_model=ListCitDiaDisponibleOut)
async def listado(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    """Días disponibles"""
    if current_user.permissions.get("CIT DIAS DISPONIBLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Entregar
    return ListCitDiaDisponibleOut(
        success=True,
        message="Listado de días disponibles",
        data=listar_dias_disponibles(database, settings),
    )
