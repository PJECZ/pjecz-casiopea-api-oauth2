"""
Cit Clientes Registros, routers
"""

import re
import uuid
from datetime import datetime, timedelta
from typing import Annotated

import pytz
import sendgrid
from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sendgrid.helpers.mail import Content, Email, Mail, To

from ..config.settings import Settings, get_settings
from ..dependencies.database import Session, get_db
from ..dependencies.pwgen import CADENA_VALIDAR_REGEXP, generar_cadena_para_validar
from ..dependencies.safe_string import safe_curp, safe_email, safe_string, safe_telefono
from ..models.cit_clientes import CitCliente
from ..models.cit_clientes_registros import CitClienteRegistro
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
    settings: Annotated[Settings, Depends(get_settings)],
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
        return OneCitClienteRegistroOut(success=False, message="No es válido el e-mail")

    # Verificar que no exista un cliente con ese correo electrónico
    if database.query(CitCliente).filter_by(email=email).first() is not None:
        return OneCitClienteRegistroOut(success=False, message="No puede registrarse porque ya hay una cuenta con ese e-mail")

    # Verificar que no exista un cliente con ese CURP
    if database.query(CitCliente).filter_by(curp=curp).first() is not None:
        return OneCitClienteRegistroOut(success=False, message="No puede registrarse porque ya hay una cuenta con ese CURP")

    # Verificar que no haya un registro pendiente con ese CURP
    posible_cit_cliente_registro = database.query(CitClienteRegistro).filter_by(curp=curp).filter_by(estatus="A").first()
    if posible_cit_cliente_registro is not None:
        return OneCitClienteRegistroOut(
            success=False,
            message=f"Ya hay un registro con ese CURP, de término o espere {EXPIRACION_HORAS} horas para que expire",
        )

    # Verificar que no haya un registro pendiente con ese correo electrónico
    posible_cit_cliente_registro = database.query(CitClienteRegistro).filter_by(email=email).filter_by(estatus="A").first()
    if posible_cit_cliente_registro is not None:
        return OneCitClienteRegistroOut(
            success=False,
            message=f"Ya hay un registro con ese e-mail, de término o espere {EXPIRACION_HORAS} horas para que expire",
        )

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

    # Elaborar el asunto del mensaje
    asunto_str = "Validar su cuenta de correo electrónico en el Sistema de Citas PJECZ"

    # Elaborar el URL de verificación
    verificacion_url = settings.NEW_ACCOUNT_WEB_PAGE_URL
    verificacion_url = f"{verificacion_url}?id={str(cit_cliente_registro.id)}"
    verificacion_url = f"{verificacion_url}&cadena_validar={cit_cliente_registro.cadena_validar}"

    # Elaborar el contenido del mensaje
    fecha_envio = datetime.now(tz=pytz.timezone(settings.TZ)).strftime("%d/%b/%Y %H:%M")
    contenidos = []
    contenidos.append(f"<h2>{asunto_str}</h2>")
    contenidos.append(f"<p>Enviado el {fecha_envio}</p>")
    contenidos.append("<p><strong>Antes de 48 horas vaya a este URL para validar y definir su contraseña:</strong></p>")
    contenidos.append("<ul>")
    contenidos.append(f"<li>{verificacion_url}</li>")
    contenidos.append("</ul>")
    contenidos.append("<p>Este mensaje fue enviado por un programa. <em>NO RESPONDA ESTE MENSAJE.</em></p>")
    contenido_html = "\n".join(contenidos)

    # Enviar el e-mail
    send_grid = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    to_email = To(cit_cliente_registro.email)
    remitente_email = Email(settings.SENDGRID_FROM_EMAIL)
    contenido = Content("text/html", contenido_html)
    mail = Mail(
        from_email=remitente_email,
        to_emails=to_email,
        subject=asunto_str,
        html_content=contenido,
    )

    # Enviar mensaje de correo electrónico
    try:
        send_grid.send(mail)
    except Exception as error:
        return OneCitClienteRegistroOut(
            success=False,
            message=f"Error al enviar el mensaje por Sendgrid: {str(error)}",
        )

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

    # Si la cadena_validar es diferente, causa error
    if cit_cliente_registro.cadena_validar != cadena_validar:
        return OneCitClienteRegistroOut(success=False, message="No es igual la cadena de validación")

    # Si ya está eliminado, causa error
    if cit_cliente_registro.estatus != "A":
        return OneCitClienteRegistroOut(success=False, message="Esta solicitud de nueva cuenta ha sido eliminada")

    # Si ya se recuperó, causa error
    if cit_cliente_registro.ya_registrado is True:
        return OneCitClienteRegistroOut(success=False, message="Esta solicitud de nueva cuenta ya fue hecha")

    # Entregar
    return OneCitClienteRegistroOut(
        success=True,
        message="Solicitud de registro de cliente validada",
        data=CitClienteRegistroOut.model_validate(cit_cliente_registro),
    )


@cit_clientes_registros.post("/terminar", response_model=OneCitClienteRegistroOut)
async def terminar(
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
    if re.match(CADENA_VALIDAR_REGEXP, terminar_cit_cliente_registro_in.password) is None:
        return OneCitClienteRegistroOut(success=False, message="No es válida la contraseña")

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
        contrasena_sha256=pwd_context.hash(terminar_cit_cliente_registro_in.password),
        renovacion=renovacion_ts.date(),
    )
    database.add(cit_cliente)
    database.commit()

    # Actualizar el registro con ya_registrado en verdadero
    cit_cliente_registro.ya_registrado = True
    database.add(cit_cliente_registro)
    database.commit()
    database.refresh(cit_cliente_registro)

    # Elaborar el asunto del mensaje
    asunto_str = "Se ha completado el registro al Sistema de Citas PJECZ"

    # Elaborar el contenido del mensaje
    fecha_envio = datetime.now(tz=pytz.timezone(settings.TZ)).strftime("%d/%b/%Y %H:%M")
    contenidos = []
    contenidos.append(f"<h2>{asunto_str}</h2>")
    contenidos.append(f"<p>Enviado el {fecha_envio}</p>")
    contenidos.append("<p><strong>Su cuenta está lista y ya puede ingresar al Sistema de Citas PJECZ</strong></p>")
    contenidos.append("<ul>")
    contenidos.append(f'<li><a href="{settings.HOST}">{settings.HOST}</a></li>')
    contenidos.append("</ul>")
    contenidos.append("<p>Use esta dirección de correo electrónico y su contraseña para ingresar.</p>")
    contenidos.append("<p>Este mensaje fue enviado por un programa. <em>NO RESPONDA ESTE MENSAJE.</em></p>")
    contenido_html = "\n".join(contenidos)

    # Enviar el e-mail
    send_grid = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    to_email = To(cit_cliente_registro.email)
    remitente_email = Email(settings.SENDGRID_FROM_EMAIL)
    contenido = Content("text/html", contenido_html)
    mail = Mail(
        from_email=remitente_email,
        to_emails=to_email,
        subject=asunto_str,
        html_content=contenido,
    )

    # Enviar mensaje de correo electrónico
    try:
        send_grid.send(mail)
    except Exception as error:
        return OneCitClienteRegistroOut(
            success=False,
            message=f"Error al enviar el mensaje por Sendgrid: {str(error)}",
        )

    # Entregar
    return OneCitClienteRegistroOut(
        success=True,
        message="Solicitud de registro de cliente terminada",
        data=CitClienteRegistroOut.model_validate(cit_cliente_registro),
    )
