class Pais:
    def __init__(self, nombre, lista_comunidades=None, lista_partidos=None):
        self.nombre = nombre
        
        # Diccionario de Comunidades Autónomas
        # Clave: ID o Nombre -> Valor: Objeto ComunidadAutonoma
        self.comunidades_autonomas = {}
        if lista_comunidades is not None:
            for clave_comunidad, objeto_comunidad in lista_comunidades:
                self.comunidades_autonomas[clave_comunidad] = objeto_comunidad
                
        # Diccionario de Partidos Políticos
        # Clave: Nombre del Partido -> Valor: Objeto Partido
        self.partidos = {}
        if lista_partidos is not None:
            for nombre_partido, objeto_partido in lista_partidos:
                self.partidos[nombre_partido] = objeto_partido



                