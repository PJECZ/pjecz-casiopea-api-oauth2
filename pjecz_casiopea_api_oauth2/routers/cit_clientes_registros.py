"""
Cit Clientes Registros, routers
"""

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..config.settings import Settings, get_settings
from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.pwgen import generar_cadena_para_validar
from ..dependencies.safe_string import safe_curp, safe_email, safe_string, safe_telefono, safe_uuid
from ..models.cit_clientes import CitCliente
from ..models.cit_clientes_registros import CitClienteRegistro
from ..models.permisos import Permiso
from ..schemas.cit_clientes import CitClienteInDB
from ..schemas.cit_clientes_registros import (
    CitClienteRegistroOut,
    OneCitClienteRegistroOut,
    SolicitarCitClienteRegistroIn,
    TerminarCitClienteRegistroIn,
    ValidarCitClienteRegistroIn,
)

EXPIRACION_HORAS = 48

cit_clientes_registros = APIRouter(prefix="/api/v5/cit_clientes_registros")


@cit_clientes_registros.post("/solicitar", response_model=OneCitClienteRegistroOut)
async def solicitar(
    database: Annotated[Session, Depends(get_db)],
    solicitar_cit_cliente_registro_in: SolicitarCitClienteRegistroIn,
):
    """Solicitar el registro de un cliente, se reciben los datos personales"""

    # Validar nombres
    nombres = safe_string(solicitar_cit_cliente_registro_in.nombres, save_enie=True)
    if nombres == "":
        return OneCitClienteRegistroOut(success=False, message="No son válidos los nombres")

    # Validar apellido_primero
    apellido_primero = safe_string(solicitar_cit_cliente_registro_in.apellido_primero, save_enie=True)
    if apellido_primero == "":
        return OneCitClienteRegistroOut(success=False, message="No es válido el primer apellido")

    # Se permite omitir el apellido_segundo
    apellido_segundo = safe_string(solicitar_cit_cliente_registro_in.apellido_segundo, save_enie=True)

    # Validar CURP
    try:
        curp = safe_curp(solicitar_cit_cliente_registro_in.curp)
    except ValueError:
        return OneCitClienteRegistroOut(success=False, message="No es válido el CURP")

    # Validar telefono
    telefono = safe_telefono(solicitar_cit_cliente_registro_in.telefono)
    if telefono == "":
        return OneCitClienteRegistroOut(success=False, message="No es válido el teléfono")

    # Validar email
    try:
        email = safe_email(solicitar_cit_cliente_registro_in.email)
    except ValueError:
        return OneCitClienteRegistroOut(success=False, message="No es válido el email")

    # Verificar que no exista un cliente con ese CURP
    if database.query(CitCliente).filter_by(curp=curp).first() is not None:
        return OneCitClienteRegistroOut(success=False, message="No puede registrarse porque ya existe una cuenta con ese CURP")

    # Verificar que no exista un cliente con ese correo electrónico
    if database.query(CitCliente).filter_by(email=email).first() is not None:
        return OneCitClienteRegistroOut(success=False, message="No puede registrarse porque ya existe una cuenta con ese email")

    # Verificar que no haya un registro pendiente con ese CURP
    if (
        database.query(CitClienteRegistro).filter_by(curp=curp).filter_by(ya_registrado=False).filter_by(estatus="A").first()
        is not None
    ):
        return OneCitClienteRegistroOut(success=False, message="Ya hay una solicitud de registro para ese CURP")

    # Verificar que no haya un registro pendiente con ese correo electrónico
    if (
        database.query(CitClienteRegistro).filter_by(email=email).filter_by(ya_registrado=False).filter_by(estatus="A").first()
        is not None
    ):
        return OneCitClienteRegistroOut(success=False, message="Ya hay una solicitud de registro para ese correo electrónico")

    # Insertar
    cit_cliente_registro = CitClienteRegistro(
        nombres=nombres,
        apellido_primero=apellido_primero,
        apellido_segundo=apellido_segundo,
        curp=curp,
        telefono=telefono,
        email=email,
        expiracion=datetime.now() + timedelta(hours=EXPIRACION_HORAS),
        cadena_validar=generar_cadena_para_validar(),
    )
    database.add(cit_cliente_registro)
    database.commit()
    database.refresh(cit_cliente_registro)

    # TODO: Agregar tarea en el fondo para que se envie un mensaje via correo electrónico

    # Entregar
    return OneCitClienteRegistroOut.model_validate(cit_cliente_registro)


@cit_clientes_registros.post("/validar_email", response_model=OneCitClienteRegistroOut)
async def validar_email(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    validar_cit_cliente_registro_in: ValidarCitClienteRegistroIn,
):
    """Validar el e-mail del registro de un cliente, ya que viene al dar clic en el enlace enviado por correo electrónico"""

    # Validar id, debe ser un UUID

    # Validar cadena_validar, debe ser una cadena de texto con minúsculas, mayúsculas y dígitos

    # Consultar

    # Si no se encuentra, causa error

    # Si ya está eliminado, causa error

    # Si ya se recuperó, causa error

    # Si la cadena_validar es diferente, causa error

    # Entregar


@cit_clientes_registros.post("/terminar", response_model=OneCitClienteRegistroOut)
async def terminar(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    terminar_cit_cliente_registro_in: TerminarCitClienteRegistroIn,
):
    """Terminar el registro de un cliente, se recibe la contraseña"""

    # Validar id, debe ser un UUID

    # Validar cadena_validar, debe ser una cadena de texto con minúsculas, mayúsculas y dígitos

    # Validar password

    # Consultar

    # Si no se encuentra, causa error

    # Si ya está eliminado, causa error

    # Si ya se recuperó, causa error

    # Si la cadena_validar es diferente, causa error

    # Si no es válido el password, causa error

    # TODO: Agregar tarea en el fondo para que se envie un mensaje via correo electrónico

    # Entregar


@cit_clientes_registros.get("/{cit_cliente_registro_id}", response_model=OneCitClienteRegistroOut)
async def detalle(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cliente_registro_id: str,
):
    """Detalle de un registro a partir de su ID"""
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
