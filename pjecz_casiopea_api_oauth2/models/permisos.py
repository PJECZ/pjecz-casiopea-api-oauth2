"""
Permisos, modelos
"""


class Permiso:
    """Permiso"""

    VER = 1
    MODIFICAR = 2
    CREAR = 3
    ADMINISTRAR = 4
    NIVELES = {
        1: "VER",
        2: "VER y MODIFICAR",
        3: "VER, MODIFICAR y CREAR",
        4: "ADMINISTRAR",
    }
