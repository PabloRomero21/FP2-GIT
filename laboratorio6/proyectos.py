class Proyecto:
    """
    Clase base que almacena la información fundamental de todos los proyectos de investigación.
    """
    
    def __init__(self, referencia: str, area: str, entidad_solicitante: str, comunidad_autonoma: str):
        # Atributos inicializados a partir de los parámetros
        self.referencia = referencia
        self.area = area
        self.entidad_solicitante = entidad_solicitante
        self.comunidad_autonoma = comunidad_autonoma
        
        # Atributo con valor por defecto según las instrucciones
        self.concedido = False


class ProyectoConcedido(Proyecto):
    """
    Clase que representa un proyecto de investigación que ha sido aprobado.
    Hereda toda la información base de la clase Proyecto.
    """
    
    def __init__(self, referencia: str, area: str, entidad_solicitante: str, 
                 comunidad_autonoma: str, costes_directos: float, 
                 costes_indirectos: float, anticipo: float, subvencion: float, 
                 anualidades: list[float], num_contratos: int):
        
        # 1. Llamada al constructor de la clase padre (Proyecto)
        super().__init__(referencia, area, entidad_solicitante, comunidad_autonoma)
        
        # 2. Modificamos el estado del atributo heredado a True
        self.concedido = True
        
        # 3. Asignación de los nuevos atributos específicos
        self.costes_directos = costes_directos
        self.costes_indirectos = costes_indirectos
        self.anticipo = anticipo
        self.subvencion = subvencion
        self.anualidades = anualidades  # Se espera una lista de 4 floats
        
        # 4. Asignación del campo booleano según el número de contratos
        self.contratado_predoctoral = num_contratos > 0
        
        # 5. Validación requerida en las instrucciones
        self._validar_importes()

    @property
    def presupuesto(self) -> float:
        """
        Propiedad derivada. Se calcula dinámicamente cada vez que se solicita.
        """
        return self.costes_directos + self.costes_indirectos

    def _validar_importes(self):
        """
        Método privado que comprueba que las sumas coinciden.
        """
        # Se usa round(, 2) para evitar los típicos errores de precisión de decimales en Python
        suma_costes = round(self.costes_directos + self.costes_indirectos, 2)
        suma_ingresos = round(self.anticipo + self.subvencion, 2)
        
        if suma_costes != suma_ingresos:
            raise ValueError(f"Error en el proyecto {self.referencia}: "
                             f"La suma de costes ({suma_costes}) no coincide con "
                             f"la suma de anticipo y subvención ({suma_ingresos}).")


class ProyectoContrato(ProyectoConcedido):
    """
    Clase que representa un proyecto concedido que incluye al menos un 
    contrato predoctoral. Hereda de ProyectoConcedido.
    """
    
    def __init__(self, referencia: str, area: str, entidad_solicitante: str, 
                 comunidad_autonoma: str, costes_directos: float, 
                 costes_indirectos: float, anticipo: float, subvencion: float, 
                 anualidades: list[float], num_contratos: int, titulo: str):
        
        # 1. Llamada al constructor de la clase padre (ProyectoConcedido)
        super().__init__(referencia, area, entidad_solicitante, comunidad_autonoma,
                         costes_directos, costes_indirectos, anticipo, subvencion,
                         anualidades, num_contratos)
        
        # 2. Añadimos el nuevo atributo específico de esta clase
        self.titulo = titulo
        
        # 3. Forzamos el valor requerido por las instrucciones
        self.contratado_predoctoral = True