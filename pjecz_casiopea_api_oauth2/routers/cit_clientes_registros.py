"""
Cit Clientes Registros, routers
"""

import re
import uuid
from datetime import datetime, timedelta
from typing import Annotated

from dependencies.authentications import PASSWORD_REGEXP
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext

from ..config.settings import Settings, get_settings
from ..dependencies.authentications import get_current_active_user
from ..dependencies.database import Session, get_db
from ..dependencies.pwgen import CADENA_VALIDAR_REGEXP, generar_cadena_para_validar
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
RENOVACION_DIAS = 365

cit_clientes_registros = APIRouter(prefix="/api/v5/cit_clientes_registros")


@cit_clientes_registros.post("/solicitar", response_model=OneCitClienteRegistroOut)
async def solicitar(
    database: Annotated[Session, Depends(get_db)],
    solicitar_cit_cliente_registro_in: SolicitarCitClienteRegistroIn,
):
    """Solicitar el registro de un cliente, se va a enviar un mensaje a su e-mail para validar que existe"""

    # Validar nombres
    nombres = safe_string(solicitar_cit_cliente_registro_in.nombres, save_enie=True)
    if nombres == "":
        return OneCitClienteRegistroOut(success=False, message="No son válidos los nombres")

    # Validar apellido_primero
    apellido_primero = safe_string(solicitar_cit_cliente_registro_in.apellido_primero, save_enie=True)
    if apellido_primero == "":
        return OneCitClienteRegistroOut(success=False, message="No es válido el primer apellido")

    # Se puede omitir apellido_segundo
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
    return OneCitClienteRegistroOut(
        success=True,
        message="Solicitud de registro de cliente creada",
        data=CitClienteRegistroOut.model_validate(cit_cliente_registro),
    )


@cit_clientes_registros.post("/validar", response_model=OneCitClienteRegistroOut)
async def validar(
    database: Annotated[Session, Depends(get_db)],
    validar_cit_cliente_registro_in: ValidarCitClienteRegistroIn,
):
    """Validar el e-mail del registro de un cliente, ya que viene al dar clic en el enlace enviado por correo electrónico"""

    # Validar ID, debe ser un UUID
    try:
        id = uuid.UUID(validar_cit_cliente_registro_in.id)
    except ValueError:
        return OneCitClienteRegistroOut(success=False, message="El ID no es válido")
    cit_cliente_registro = database.query(CitClienteRegistro).get(id)
    if cit_cliente_registro is None:
        return OneCitClienteRegistroOut(success=False, message="No existe ese registro")

    # Validar cadena_validar, debe ser una cadena de texto con minúsculas, mayúsculas y dígitos
    cadena_validar = safe_string(validar_cit_cliente_registro_in.cadena_validar, to_uppercase=False)
    if re.match(CADENA_VALIDAR_REGEXP, cadena_validar) is None:
        return OneCitClienteRegistroOut(success=False, message="La cadena de validación no es válida")

    # Consultar, si no se encuentra causa error
    cit_cliente_registro = database.query(CitClienteRegistro).get(id)
    if cit_cliente_registro is None:
        return OneCitClienteRegistroOut(success=False, message="No existe la solicitud de una nueva cuenta con el ID dado")

    # Si ya está eliminado, causa error
    if cit_cliente_registro.estatus != "A":
        return OneCitClienteRegistroOut(success=False, message="Esta solicitud de nueva cuenta ha sido eliminada")

    # Si ya se recuperó, causa error
    if cit_cliente_registro.ya_registrado is True:
        return OneCitClienteRegistroOut(success=False, message="Esta solicitud de nueva cuenta ya fue hecha")

    # Si la cadena_validar es diferente, causa error
    if cit_cliente_registro.cadena_validar != cadena_validar:
        return OneCitClienteRegistroOut(success=False, message="No es igual la cadena de validación")

    # Entregar
    return OneCitClienteRegistroOut(
        success=True,
        message="Solicitud de registro de cliente validada",
        data=CitClienteRegistroOut.model_validate(cit_cliente_registro),
    )


@cit_clientes_registros.post("/terminar", response_model=OneCitClienteRegistroOut)
async def terminar(
    current_user: Annotated[CitClienteInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    terminar_cit_cliente_registro_in: TerminarCitClienteRegistroIn,
):
    """Terminar el registro de un cliente, se recibe la contraseña"""

    # Validar ID, debe ser un UUID
    try:
        id = uuid.UUID(terminar_cit_cliente_registro_in.id)
    except ValueError:
        return OneCitClienteRegistroOut(success=False, message="El ID no es válido")
    cit_cliente_registro = database.query(CitClienteRegistro).get(id)
    if cit_cliente_registro is None:
        return OneCitClienteRegistroOut(success=False, message="No existe ese registro")

    # Validar cadena_validar, debe ser una cadena de texto con minúsculas, mayúsculas y dígitos
    cadena_validar = safe_string(terminar_cit_cliente_registro_in.cadena_validar, to_uppercase=False)
    if re.match(CADENA_VALIDAR_REGEXP, cadena_validar) is None:
        return OneCitClienteRegistroOut(success=False, message="La cadena de validación no es válida")

    # Consultar, si no se encuentra causa error
    cit_cliente_registro = database.query(CitClienteRegistro).get(id)
    if cit_cliente_registro is None:
        return OneCitClienteRegistroOut(success=False, message="No existe la solicitud de una nueva cuenta con el ID dado")

    # Si ya está eliminado, causa error
    if cit_cliente_registro.estatus != "A":
        return OneCitClienteRegistroOut(success=False, message="Esta solicitud de nueva cuenta ha sido eliminada")

    # Si ya se recuperó, causa error
    if cit_cliente_registro.ya_registrado is True:
        return OneCitClienteRegistroOut(success=False, message="Esta solicitud de nueva cuenta ya fue hecha")

    # Si la cadena_validar es diferente, causa error
    if cit_cliente_registro.cadena_validar != cadena_validar:
        return OneCitClienteRegistroOut(success=False, message="No es igual la cadena de validación")

    # Si no es válido el password, causa error
    if re.match(PASSWORD_REGEXP, terminar_cit_cliente_registro_in.password) is None:
        return OneCitClienteRegistroOut(success=False, message="No es válido el password")

    # Cifrar la contrasena
    pwd_context = CryptContext(schemes=["pbkdf2_sha256", "des_crypt"], deprecated="auto")

    # Definir el tiempo de renovacion
    renovacion_ts = datetime.now() + timedelta(days=RENOVACION_DIAS)

    # Insertar cliente
    cit_cliente = CitCliente(
        nombres=cit_cliente_registro.nombres,
        apellido_primero=cit_cliente_registro.apellido_primero,
        apellido_segundo=cit_cliente_registro.apellido_segundo,
        curp=cit_cliente_registro.curp,
        telefono=cit_cliente_registro.telefono,
        email=cit_cliente_registro.email,
        contrasena_md5="",
        contrasena_sha256=pwd_context.hash(cit_cliente_registro.password),
        renovacion=renovacion_ts.date(),
    )
    database.add(cit_cliente)
    database.commit()

    # Actualizar el registro con ya_registrado en verdadero
    cit_cliente_registro.ya_registrado = True
    database.add(cit_cliente_registro)
    database.commit()
    database.refresh(cit_cliente_registro)

    # TODO: Agregar tarea en el fondo para que se envie un mensaje via correo electrónico

    # Entregar
    return OneCitClienteRegistroOut(
        success=True,
        message="Solicitud de registro de cliente terminada",
        data=CitClienteRegistroOut.model_validate(cit_cliente_registro),
    )


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
