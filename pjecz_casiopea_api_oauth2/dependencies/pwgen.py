"""
Generador de contraseñas
"""

import random
import string


def generar_codigo_asistencia(largo=4):
    """Generar codigo asistencia"""
    digitos = string.digits
    temp = random.sample(digitos, largo)
    return "".join(temp)
