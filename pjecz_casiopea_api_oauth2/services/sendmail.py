"""
Servicio para enviar correos electrónicos
"""
import os
from abc import ABC, abstractmethod
from datetime import datetime
import pytz

from jinja2 import Environment, FileSystemLoader

import sendgrid
from sendgrid.helpers.mail import Content, Email as EmailSendGrid, Mail, To
from ..config.settings import Settings, get_settings


class PlantillaEmailBase(ABC):
    """Clase base abstracta para las plantillas de correo."""

    _enviroment: Environment

    @property
    @abstractmethod
    def template_name(self) -> str:
        """Nombre del archivo de la plantilla Jinja2."""
        pass

    @property
    @abstractmethod
    def subject(self) -> str:
        """Asunto del correo electrónico."""
        pass
    
    @property
    @abstractmethod
    def _variables_contenido(self) -> dict[str, str]:
        """Variables para la plantilla."""
        pass

    def __init__(self):
        """Constructor de la clase."""

        # Por defecto se establece al fecha de envío en el momento de creación de la plantilla
        self._variables_contenido["fecha_envio_str"] = datetime.now().strftime("%d/%b/%Y %H:%M")

        # Configurar el entorno de Jinja2 para cargar plantillas desde el directorio 'templates/email'
        # La ruta se construye de forma relativa a la ubicación de este archivo.
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates', 'email')
        self._enviroment = Environment(loader=FileSystemLoader(template_dir), autoescape=True)

    def set_fecha_envio(self, fecha_envio:datetime) -> None:
        """Establece la fecha y hora de envío"""
        
        self._variables_contenido["fecha_envio_str"] = fecha_envio.strftime("%d/%b/%Y %H:%M")

    @abstractmethod
    def get_contenido(self) -> dict:
        """Diccionario con las variables para renderizar la plantilla."""
        pass

    def get_contenido(self) -> Content:
        """Carga las variables en la plantilla y la regresa como contenido HTML"""

        # Cargar la plantilla específica
        template = self._enviroment.get_template(self.template_name)
        # Renderizar la plantilla con las variables proporcionadas
        return Content("text/html", template.render(**self._variables_contenido))


class PlantillaClienteRecuperacionContrasena(PlantillaEmailBase):
    """
    Define los datos necesarios para la plantilla de recuperación de contraseña para un cliente.
    """
    template_name = "cliente_recuperacion_contrasena.jinja2"
    subject = "Cambiar su contraseña en el Sistema de Citas PJECZ"
    _variables_contenido: dict[str, str] = {
        'asunto': '',
        'fecha_envio': '',
        'verificacion_url': '',
    }

    def __init__(self, asunto: str, verificacion_url: str):
        super().__init__()

        self._variables_contenido['asunto'] = asunto
        self._variables_contenido['verificacion_url'] = verificacion_url


class PlantillaCitaCreada(PlantillaEmailBase):
    """
    Plantilla para la creación de una cita.
    """
    template_name = "cita_creada.jinja2"
    subject = "Cita Agendada en el Sistema de Citas PJECZ"
    _variables_contenido: dict[str, str] = {
        'fecha_envio': '',
        'id': '',
        'nombre_cliente': '',
        'oficina': '',
        'servicio': '',
        'fecha_cita': '',
        'hora_cita': '',
        'notas': '',
        'codigo_qr': '',
        'codigo_asistencia': 0,
    }

    def __init__(self, id: str, nombre_cliente: str, oficina: str, servicio: str, fecha_cita: str, hora_cita: str, notas: str, codigo_qr: str, codigo_asistencia: int):
        super().__init__()

        self._variables_contenido['id'] = id
        self._variables_contenido['nombre_cliente'] = nombre_cliente
        self._variables_contenido['oficina'] = oficina
        self._variables_contenido['servicio'] = servicio
        self._variables_contenido['fecha_cita'] = fecha_cita
        self._variables_contenido['hora_cita'] = hora_cita
        self._variables_contenido['notas'] = notas
        self._variables_contenido['codigo_qr'] = codigo_qr
        self._variables_contenido['codigo_asistencia'] = codigo_asistencia


class Email():
    """Email"""

    _settings: Settings
    _remitente_email: EmailSendGrid
    plantilla: PlantillaEmailBase
    to_email: To

    def __init__(self, to_email: str, plantilla: PlantillaEmailBase):
        """Constructor de la clase"""

        self._settings = get_settings()
        self._remitente_email = EmailSendGrid(self._settings.SENDGRID_FROM_EMAIL)

        self.plantilla = plantilla
        self.to_email = To(to_email)


    def enviar_email(self):
        """ Envío de email por SendGrid """

        # Establecer la fecha y hora de envío
        self.plantilla.set_fecha_envio(datetime.now(tz=pytz.timezone(self._settings.TZ)))

        # Enviar el e-mail
        send_grid = sendgrid.SendGridAPIClient(api_key=self._settings.SENDGRID_API_KEY)
        
        mail = Mail(
            from_email=self._remitente_email,
            to_emails=self.to_email,
            subject=self.plantilla.subject,
            html_content=self.plantilla.get_contenido(),
        )

        # Enviar mensaje de correo electrónico
        send_grid.send(mail)
