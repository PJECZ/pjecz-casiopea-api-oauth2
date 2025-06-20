"""
Control de Accesos es la API para obtener el código de acceso como una imagen de un QR
"""

import base64
import hashlib
import re
from datetime import datetime


def generar_referencia(cit_cliente_email: str, cit_servicio_clave: str, oficina_clave: str, inicio: datetime) -> str:
    """Generar una referencia para solicitar un código de acceso"""
    data_string = f"{cit_cliente_email}-{cit_servicio_clave}-{oficina_clave}-{inicio.isoformat()}"
    return hashlib.sha256(data_string.encode()).hexdigest()


def decodificar_imagen(data_uri_string: str) -> bytes:
    """Decodificar la imagen que viene en data_uri_str"""

    # Separar con una expresión regular el MIME/TYPE de la imagen codificada en base64
    match = re.match(r"data:(?P<mime_type>[^;]+);base64,(?P<data>.+)", data_uri_string)
    if not match:
        raise ValueError("ERROR: Invalid data URI format.")
    mime_type = match.group("mime_type")
    base64_data = match.group("data")

    # Validar mime_type como image/png
    if mime_type != "image/png":
        raise ValueError("ERROR: Invalid image mime type.")

    # Decodificar
    try:
        decoded_image_data = base64.b64decode(base64_data)
    except (base64.binascii.Error, base64.binascii.Incomplete, ValueError):
        raise ValueError("ERROR: Invalid base64 data.")

    # Entregar
    return decoded_image_data
