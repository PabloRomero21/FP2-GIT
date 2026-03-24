class ComunidadAutonoma:
    def __init__(self, nombre, lista_provincias=None):
        self.nombre = nombre
        
        # Inicializamos el diccionario vacío internamente
        self.provincias = {}
        
        # Si recibimos la lista de tuplas (id, objeto_provincia), la procesamos
        if lista_provincias is not None:
            for id_provincia, objeto_provincia in lista_provincias:
                self.provincias[id_provincia] = objeto_provincia

    @property
    def porcentaje_nulos_blancos(self):
        """Propiedad derivada: Agrupa los datos de sus provincias y calcula el porcentaje autonómico."""
        total_invalidos = 0
        total_votantes = 0
        
        for provincia in self.provincias.values():
            total_invalidos += (provincia.votos_en_blanco + provincia.votos_en_nulo)
            total_votantes += provincia.total_votantes
            
        if total_votantes == 0:
            return 0.0
            
        return (total_invalidos / total_votantes) * 100
    

    @property
    def participacion_cera(self):
        """Agrupa los datos CERA de sus provincias y calcula el porcentaje autonómico."""
        total_censo_cera = 0
        total_votantes_cera = 0
        
        for provincia in self.provincias.values():
            total_censo_cera += provincia.censo_cera
            total_votantes_cera += provincia.total_votantes_cera
            
        if total_censo_cera == 0:
            return 0.0
            
        return (total_votantes_cera / total_censo_cera) * 100
    


    @property
    def proporcion_votantes_cera_poblacion(self):
        """
        Calcula el % de votantes CERA (extranjero) con respecto 
        a la población total de la comunidad autónoma.
        """
        total_poblacion = 0
        total_votantes_cera = 0
        
        for provincia in self.provincias.values():
            total_poblacion += provincia.poblacion
            total_votantes_cera += provincia.total_votantes_cera
            
        # Evitamos divisiones por cero por seguridad
        if total_poblacion == 0:
            return 0.0
            
        return (total_votantes_cera / total_poblacion) * 100