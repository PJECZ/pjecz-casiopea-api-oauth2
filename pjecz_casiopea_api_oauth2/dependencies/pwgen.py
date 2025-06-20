"""
Generador de contraseñas
"""

import random
import string

CADENA_VALIDAR_REGEXP = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,24}$"
CODIGO_ASISTENCIA_REGEXP = r"^\d{4,8}$"


def generar_cadena_para_validar(largo: int = 24) -> str:
    """Generar cadena de texto aleatorio con minúsculas, mayúsculas y dígitos"""
    minusculas = string.ascii_lowercase
    mayusculas = string.ascii_uppercase
    digitos = string.digits
    todos = minusculas + mayusculas + digitos
    temp = random.sample(todos, largo)
    return "".join(temp)


def generar_codigo_asistencia(largo: int = 6) -> str:
    """Generar codigo asistencia"""
    digitos = string.digits
    temp = random.sample(digitos, largo)
    return "".join(temp)
