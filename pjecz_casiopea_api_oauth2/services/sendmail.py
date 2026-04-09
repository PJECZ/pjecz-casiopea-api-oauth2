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
    _fecha_envio_str: str

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

    def __init__(self):
        """Constructor de la clase."""

        # Por defecto se establece al fecha de envío en el momento de creación de la plantilla
        self._fecha_envio_str = datetime.now().strftime("%d/%b/%Y %H:%M")

        # Configurar el entorno de Jinja2 para cargar plantillas desde el directorio 'templates/email'
        # La ruta se construye de forma relativa a la ubicación de este archivo.
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates', 'email')
        self._enviroment = Environment(loader=FileSystemLoader(template_dir), autoescape=True)

    def set_fecha_envio(self, fecha_envio:datetime) -> None:
        """Establece la fecha y hora de envío"""
        
        self._fecha_envio_str = fecha_envio.strftime("%d/%b/%Y %H:%M")

    @abstractmethod
    def get_contenido(self) -> dict:
        """Diccionario con las variables para renderizar la plantilla."""
        pass

    @abstractmethod
    def get_contenido(self) -> Content:
        """Regresa el contenido de la plantilla con las variables cargadas."""
        pass


class PlantillaClienteRecuperacionContrasena(PlantillaEmailBase):
    """
    Define los datos necesarios para la plantilla de recuperación de contraseña para un cliente.
    Valida en el constructor que todos los datos requeridos son proporcionados.
    """
    template_name = "cliente_recuperacion_contrasena.jinja2"
    subject = "Cambiar su contraseña en el Sistema de Citas PJECZ"
    _variables_contenido: dict[str, str] = {
        'asunto': '',
        'fecha_envio': '',
        'verificacion_url': '',
    }

    def __init__(self, verificacion_url: str):
        super().__init__()
        self._variables_contenido['verificacion_url'] = verificacion_url
    
    def get_contenido(self) -> Content:
        """Carga las variables en la plantilla y la regresa como contenido HTML"""

        # Cargar la plantilla específica
        template = self._enviroment.get_template(self.template_name)

        # Variable de asunto
        self._variables_contenido['asunto'] = self.subject

        # Renderizar la plantilla con las variables proporcionadas
        return Content("text/html", template.render(**self._variables_contenido))


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
