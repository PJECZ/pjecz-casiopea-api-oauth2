"""
Cit Clientes Recuperaciones, routers
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
from ..dependencies.safe_string import safe_email, safe_string
from ..models.cit_clientes import CitCliente
from ..models.cit_clientes_recuperaciones import CitClienteRecuperacion
from ..schemas.cit_clientes_recuperaciones import (
    CitClienteRecuperacionOut,
    OneCitClienteRecuperacionOut,
    SolicitarCitClienteRecuperacionIn,
    TerminarCitClienteRecuperacionIn,
    ValidarCitClienteRecuperacionIn,
)

EXPIRACION_HORAS = 48
RENOVACION_DIAS = 365

cit_clientes_recuperaciones = APIRouter(prefix="/api/v5/cit_clientes_recuperaciones")


@cit_clientes_recuperaciones.post("/solicitar", response_model=OneCitClienteRecuperacionOut)
async def solicitar(
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    solicitar_cit_cliente_recuperacion_in: SolicitarCitClienteRecuperacionIn,
):
    """Solicitar una recuperación de contraseña"""

    # Validar email
    try:
        email = safe_email(solicitar_cit_cliente_recuperacion_in.email)
    except ValueError:
        return OneCitClienteRecuperacionOut(success=False, message="No es válido el e-mail")

    # Validar que exista el cliente con ese correo electrónico
    cit_cliente = database.query(CitCliente).filter_by(email=email).first()
    if cit_cliente is None:
        return OneCitClienteRecuperacionOut(success=False, message="No existe esa cuenta con ese e-mail")

    # Validar que NO exista una recuperación pendiente
    posible_cit_cliente_recuperacion = (
        database.query(CitClienteRecuperacion).filter_by(cit_cliente_id=cit_cliente.id).filter_by(estatus="A").first()
    )
    if posible_cit_cliente_recuperacion is not None:
        return OneCitClienteRecuperacionOut(
            success=False,
            message=f"Ya hay una recuperación de esa cuenta, de término o espere {EXPIRACION_HORAS} horas para que expire",
        )

    # Insertar
    cit_cliente_recuperacion = CitClienteRecuperacion(
        cit_cliente_id=cit_cliente.id,
        expiracion=datetime.now() + timedelta(hours=EXPIRACION_HORAS),
        cadena_validar=generar_cadena_para_validar(),
        mensajes_cantidad=0,
        ya_recuperado=False,
    )
    database.add(cit_cliente_recuperacion)
    database.commit()
    database.refresh(cit_cliente_recuperacion)

    # Elaborar el asunto del mensaje
    asunto_str = "Cambiar su contraseña en el Sistema de Citas PJECZ"

    # Elaborar el URL de verificación
    verificacion_url = settings.RECOVER_WEB_PAGE_URL
    verificacion_url = f"{verificacion_url}?id={str(cit_cliente_recuperacion.id)}"
    verificacion_url = f"{verificacion_url}&cadena_validar={cit_cliente_recuperacion.cadena_validar}"

    # Elaborar el contenido del mensaje
    fecha_envio = datetime.now(tz=pytz.timezone(settings.TZ)).strftime("%d/%b/%Y %H:%M")
    contenidos = []
    contenidos.append(f"<h2>{asunto_str}</h2>")
    contenidos.append(f"<p>Enviado el {fecha_envio}</p>")
    contenidos.append("<p><strong>Antes de 48 horas vaya a este URL para cambiar su contraseña:</strong></p>")
    contenidos.append("<ul>")
    contenidos.append(f"<li>{verificacion_url}</li>")
    contenidos.append("</ul>")
    contenidos.append("<p>Este mensaje fue enviado por un programa. <em>NO RESPONDA ESTE MENSAJE.</em></p>")
    contenido_html = "\n".join(contenidos)

    # Enviar el e-mail
    send_grid = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    to_email = To(cit_cliente_recuperacion.email)
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
        return OneCitClienteRecuperacionOut(
            success=False,
            message=f"Error al enviar el mensaje por Sendgrid: {str(error)}",
        )

    # Entregar
    return OneCitClienteRecuperacionOut(
        success=True,
        message="Solicitud de recuperación creada",
        data=CitClienteRecuperacionOut.model_validate(cit_cliente_recuperacion),
    )


@cit_clientes_recuperaciones.post("/validar", response_model=OneCitClienteRecuperacionOut)
async def validar(
    database: Annotated[Session, Depends(get_db)],
    validar_cit_cliente_recuperacion_in: ValidarCitClienteRecuperacionIn,
):
    """Validar una recuperación de contraseña"""

    # Validar ID, debe ser un UUID
    try:
        id = uuid.UUID(validar_cit_cliente_recuperacion_in.id)
    except ValueError:
        return OneCitClienteRecuperacionOut(success=False, message="El ID no es válido")
    cit_cliente_recuperacion = database.query(CitClienteRecuperacion).get(id)
    if cit_cliente_recuperacion is None:
        return OneCitClienteRecuperacionOut(success=False, message="No existe esa recuperación")

    # Validar cadena_validar, debe ser una cadena de texto con minúsculas, mayúsculas y dígitos
    cadena_validar = safe_string(validar_cit_cliente_recuperacion_in.cadena_validar, to_uppercase=False)
    if re.match(CADENA_VALIDAR_REGEXP, cadena_validar) is None:
        return OneCitClienteRecuperacionOut(success=False, message="La cadena de validación no es válida")

    # Si la cadena_validar es diferente, causa error
    if cit_cliente_recuperacion.cadena_validar != cadena_validar:
        return OneCitClienteRecuperacionOut(success=False, message="No es igual la cadena de validación")

    # Si ya está eliminado, causa error
    if cit_cliente_recuperacion.estatus != "A":
        return OneCitClienteRecuperacionOut(success=False, message="Esta recuperación ha sido eliminada")

    # Si ya se recuperó, causa error
    if cit_cliente_recuperacion.ya_recuperado is True:
        return OneCitClienteRecuperacionOut(success=False, message="Esta recuperación ya fue hecha")

    # Entregar
    return OneCitClienteRecuperacionOut(
        success=True,
        message="Solicitud de recuperación validada",
        data=CitClienteRecuperacionOut.model_validate(cit_cliente_recuperacion),
    )


@cit_clientes_recuperaciones.post("/terminar", response_model=OneCitClienteRecuperacionOut)
async def terminar(
    database: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    terminar_cit_cliente_recuperacion_in: TerminarCitClienteRecuperacionIn,
):
    """Terminar la recuperación, se recibe la contraseña"""

    # Validar ID, debe ser un UUID
    try:
        id = uuid.UUID(terminar_cit_cliente_recuperacion_in.id)
    except ValueError:
        return OneCitClienteRecuperacionOut(success=False, message="El ID no es válido")
    cit_cliente_recuperacion = database.query(CitClienteRecuperacion).get(id)
    if cit_cliente_recuperacion is None:
        return OneCitClienteRecuperacionOut(success=False, message="No existe esa recuperación")

    # Validar cadena_validar, debe ser una cadena de texto con minúsculas, mayúsculas y dígitos
    cadena_validar = safe_string(terminar_cit_cliente_recuperacion_in.cadena_validar, to_uppercase=False)
    if re.match(CADENA_VALIDAR_REGEXP, cadena_validar) is None:
        return OneCitClienteRecuperacionOut(success=False, message="La cadena de validación no es válida")

    # Si ya está eliminado, causa error
    if cit_cliente_recuperacion.estatus != "A":
        return OneCitClienteRecuperacionOut(success=False, message="Esta recuperación ha sido eliminada")

    # Si ya se recuperó, causa error
    if cit_cliente_recuperacion.ya_recuperado is True:
        return OneCitClienteRecuperacionOut(success=False, message="Esta recuperación ya fue hecha")

    # Si la cadena_validar es diferente, causa error
    if cit_cliente_recuperacion.cadena_validar != cadena_validar:
        return OneCitClienteRecuperacionOut(success=False, message="No es igual la cadena de validación")

    # Si no es válido el password, causa error
    if re.match(CADENA_VALIDAR_REGEXP, terminar_cit_cliente_recuperacion_in.password) is None:
        return OneCitClienteRecuperacionOut(success=False, message="No es válida la contraseña")

    # Cifrar la contrasena
    pwd_context = CryptContext(schemes=["pbkdf2_sha256", "des_crypt"], deprecated="auto")

    # Definir el tiempo de renovacion
    renovacion_ts = datetime.now() + timedelta(days=RENOVACION_DIAS)

    # Actualizar el cliente
    cit_cliente = cit_cliente_recuperacion.cit_cliente
    cit_cliente.contrasena_md5 = ""
    cit_cliente.contrasena_sha256 = pwd_context.hash(terminar_cit_cliente_recuperacion_in.password)
    cit_cliente.renovacion = renovacion_ts.date()
    database.add(cit_cliente)
    database.commit()

    # Actualizar la recuperacion
    cit_cliente_recuperacion.ya_recuperado = True
    database.add(cit_cliente_recuperacion)
    database.commit()
    database.refresh(cit_cliente_recuperacion)

    # Elaborar el asunto del mensaje
    asunto_str = "Se ha completado el cambio de contraseña al Sistema de Citas PJECZ"

    # Elaborar el contenido del mensaje
    fecha_envio = datetime.now(tz=pytz.timezone(settings.TZ)).strftime("%d/%b/%Y %H:%M")
    contenidos = []
    contenidos.append(f"<h2>{asunto_str}</h2>")
    contenidos.append(f"<p>Enviado el {fecha_envio}</p>")
    contenidos.append("<p><strong>Ha cambiado su contraseña y ya puede ingresar al Sistema de Citas PJECZ</strong></p>")
    contenidos.append("<ul>")
    contenidos.append(f'<li><a href="{settings.HOST}">{settings.HOST}</a></li>')
    contenidos.append("</ul>")
    contenidos.append("<p>Este mensaje fue enviado por un programa. <em>NO RESPONDA ESTE MENSAJE.</em></p>")
    contenido_html = "\n".join(contenidos)

    # Enviar el e-mail
    send_grid = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    to_email = To(cit_cliente_recuperacion.email)
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
        return OneCitClienteRecuperacionOut(
            success=False,
            message=f"Error al enviar el mensaje por Sendgrid: {str(error)}",
        )

    # Entregar
    return OneCitClienteRecuperacionOut(
        success=True,
        message="Solicitud de recuperación terminada",
        data=CitClienteRecuperacionOut.model_validate(cit_cliente_recuperacion),
    )
