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
from ..dependencies.exceptions import MyRequestError


class PlantillaEmailBase(ABC):
    """Clase base abstracta para las plantillas de correo."""

    _enviroment: Environment
    _fecha_hora_envio_str: str

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
        self.set_fecha_envio(datetime.now())

        # Configurar el entorno de Jinja2 para cargar plantillas desde el directorio 'templates/email'
        # La ruta se construye de forma relativa a la ubicación de este archivo.
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates', 'email')
        self._enviroment = Environment(loader=FileSystemLoader(template_dir), autoescape=True)

    def set_fecha_envio(self, fecha_envio:datetime) -> None:
        """Establece la fecha y hora de envío"""
        
        self._fecha_hora_envio_str = fecha_envio.strftime("%d-%b-%Y %H:%M %p")

    @abstractmethod
    def get_contenido(self) -> dict:
        """Diccionario con las variables para renderizar la plantilla."""
        pass

    def get_contenido(self) -> Content:
        """Carga las variables en la plantilla y la regresa como contenido HTML"""

        # Cargar la plantilla específica
        template = self._enviroment.get_template(self.template_name)
        # Renderizar la plantilla con las variables proporcionadas
        return Content("text/html", template.render(**self._variables_contenido, fecha_hora_envio=self._fecha_hora_envio_str))


class PlantillaClienteValidarCuenta(PlantillaEmailBase):
    """
    Define los datos necesarios para la plantilla de validación de una cuenta de un cliente.
    """
    template_name = "cliente_validar_cuenta.jinja2"
    subject = "Valida tu email para utilizar el Sistema de Citas PJECZ"
    _variables_contenido: dict[str, str] = {
        'nombre_cliente': '',
        'cliente_id': '',
        'url_sistema_citas': '',
    }

    def __init__(self, nombre_cliente: str, cliente_id: str, url_sistema_citas: str):
        super().__init__()

        self._variables_contenido['nombre_cliente'] = nombre_cliente
        self._variables_contenido['cliente_id'] = cliente_id
        self._variables_contenido['url_sistema_citas'] = url_sistema_citas


class PlantillaClienteCambiarContrasena(PlantillaEmailBase):
    """
    Define los datos necesarios para la plantilla de cambio de contraseña de un cliente.
    """
    template_name = "cliente_cambiar_contrasena.jinja2"
    subject = "Cambiar su contraseña del Sistema de Citas PJECZ"
    _variables_contenido: dict[str, str] = {
        'nombre_cliente': '',
        'cliente_id': '',
        'cliente_email': '',
        'url_cambio_contrasena': '',
    }

    def __init__(self, nombre_cliente: str, cliente_id: str, cliente_email: str, url_cambio_contrasena: str):
        super().__init__()

        self._variables_contenido['nombre_cliente'] = nombre_cliente
        self._variables_contenido['cliente_id'] = cliente_id
        self._variables_contenido['cliente_email'] = cliente_email
        self._variables_contenido['url_cambio_contrasena'] = url_cambio_contrasena


class PlantillaClienteCompletado(PlantillaEmailBase):
    """
    Representa la plantilla de correo electrónico para notificar a un cliente
    que su proceso o registro ha sido completado con éxito.
    """

    template_name = "cliente_completado.jinja2"
    subject = "Se ha completado el registro en el Sistema de Citas PJECZ"
    _variables_contenido: dict[str, str] = {
        'nombre_cliente': '',
        'cliente_id': '',
        'cliente_email': '',
        'url_sistema_citas': '',
    }

    def __init__(self, nombre_cliente: str, cliente_id: str, cliente_email: str, url_sistema_citas: str):
        """
        Representa la plantilla de correo electrónico para notificar a un cliente
        que su proceso o registro ha sido completado con éxito.

        Esta clase hereda de `PlantillaEmailBase` y extiende su funcionalidad para
        personalizar el contenido del mensaje con los datos específicos del cliente
        y el acceso al sistema de citas.

        ## Atributos:
            nombre_cliente (str): Nombre completo del cliente para el saludo.
            cliente_id (str): Identificador único del cliente en la base de datos.
            cliente_email (str): Dirección de correo electrónico del destinatario.
            url_sistema_citas (str): Enlace directo para que el cliente gestione sus citas.

        ## Ejemplo:
        ```python
        plantilla = PlantillaClienteCompletado(
            nombre_cliente="Juan Pérez",
            cliente_id="CLI-123",
            cliente_email="juan.perez@email.com",
            url_sistema_citas="https://citas.empresa.com"
        )
        ```
        """
        super().__init__()

        self._variables_contenido['asunombre_clienteto'] = nombre_cliente
        self._variables_contenido['cliente_id'] = cliente_id
        self._variables_contenido['cliente_email'] = cliente_email
        self._variables_contenido['url_sistema_citas'] = url_sistema_citas


class PlantillaCitaCreada(PlantillaEmailBase):
    """
    Plantilla para la creación de una cita.
    """
    template_name = "cita_creada.jinja2"
    subject = "Cita Agendada en el Sistema de Citas PJECZ"
    _variables_contenido: dict[str, str] = {
        'nombre_cliente': '',
        'id': '',
        'oficina': '',
        'servicio': '',
        'fecha_hora_cita': '',
        'notas': '',
        'codigo_qr_url': '',
    }

    def __init__(self, id: str, nombre_cliente: str, oficina: str, servicio: str, fecha_hora_cita: str, notas: str, codigo_qr_url: str):
        super().__init__()

        self._variables_contenido['id'] = id
        self._variables_contenido['nombre_cliente'] = nombre_cliente
        self._variables_contenido['oficina'] = oficina
        self._variables_contenido['servicio'] = servicio
        self._variables_contenido['fecha_hora_cita'] = fecha_hora_cita
        self._variables_contenido['notas'] = notas
        self._variables_contenido['codigo_qr_url'] = codigo_qr_url


class PlantillaCitaCancelada(PlantillaEmailBase):
    """
    Plantilla para la cancelación de una cita.
    """
    template_name = "cita_cancelada.jinja2"
    subject = "Cita Cancelada en el Sistema de Citas PJECZ"
    _variables_contenido: dict[str, str] = {
        'nombre_cliente': '',
        'id': '',
        'oficina': '',
        'servicio': '',
        'fecha_hora_cita': '',
        'notas': '',
        'fecha_hora_cancelacion': '',
    }

    def __init__(self, id: str, nombre_cliente: str, oficina: str, servicio: str, fecha_hora_cita: str, notas: str, fecha_hora_cancelacion: str):
        super().__init__()

        self._variables_contenido['id'] = id
        self._variables_contenido['nombre_cliente'] = nombre_cliente
        self._variables_contenido['oficina'] = oficina
        self._variables_contenido['servicio'] = servicio
        self._variables_contenido['fecha_hora_cita'] = fecha_hora_cita
        self._variables_contenido['notas'] = notas
        self._variables_contenido['fecha_hora_cancelacion'] = fecha_hora_cancelacion


class Email():
    """Email"""

    _settings: Settings
    _remitente_email: EmailSendGrid
    plantilla: PlantillaEmailBase
    to_email: To

    def __init__(self, to_email: str, plantilla: PlantillaEmailBase = None):
        """Inicializa el servicio de email, especifica el destinatario y si quieres una plantilla"""

        self._settings = get_settings()
        self._remitente_email = EmailSendGrid(self._settings.SENDGRID_FROM_EMAIL)

        self.plantilla = plantilla
        self.to_email = To(to_email)

    def set_plantilla(self, plantilla: PlantillaEmailBase) -> None:
        """Establece una nueva plantilla a utilizar"""
        self.plantilla = plantilla

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
        try:
            send_grid.send(mail)
        except Exception as error:
            raise MyRequestError(f"Error al enviar el mensaje por Sendgrid: {str(error)}") from error
