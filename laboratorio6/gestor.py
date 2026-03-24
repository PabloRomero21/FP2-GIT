# Importamos las clases creadas anteriormente (asumiendo que están en proyectos.py)
from proyectos import Proyecto, ProyectoConcedido, ProyectoContrato

class Gestor_Proyectos:
    """
    Contenedor general para TODOS los proyectos (tanto concedidos como denegados).
    """
    def __init__(self):
        # Inicializamos el diccionario vacío. 
        # Clave: referencia (str) -> Valor: objeto Proyecto
        self.proyectos: dict[str, Proyecto] = {}

    def agregar_proyecto(self, proyecto: Proyecto):
        """Añade un proyecto al diccionario usando su referencia como clave."""
        self.proyectos[proyecto.referencia] = proyecto

    def obtener_total(self) -> int:
        """Devuelve el número total de proyectos almacenados."""
        return len(self.proyectos)


class Gestor_ProyectosConcedidos:
    """
    Contenedor exclusivo para los proyectos que han sido concedidos.
    """
    def __init__(self):
        # Clave: referencia (str) -> Valor: objeto ProyectoConcedido
        self.proyectos_concedidos: dict[str, ProyectoConcedido] = {}

    def agregar_proyecto(self, proyecto: ProyectoConcedido):
        self.proyectos_concedidos[proyecto.referencia] = proyecto

    def obtener_total(self) -> int:
        return len(self.proyectos_concedidos)


class Gestor_ProyectosContrato:
    """
    Contenedor exclusivo para los proyectos concedidos con contrato predoctoral.
    """
    def __init__(self):
        # Clave: referencia (str) -> Valor: objeto ProyectoContrato
        self.proyectos_contrato: dict[str, ProyectoContrato] = {}

    def agregar_proyecto(self, proyecto: ProyectoContrato):
        self.proyectos_contrato[proyecto.referencia] = proyecto

    def obtener_total(self) -> int:
        return len(self.proyectos_contrato)