class Partido:
    def __init__(self, nombre, datos_resultados=None):
        self.nombre = nombre
        
        # Diccionario principal:
        # Clave: Nombre Comunidad -> Valor: Diccionario de provincias
        #   Diccionario de provincias: Clave: Nombre Provincia -> Valor: (votos, diputados)
        self.resultados_por_comunidad = {}
        
        if datos_resultados is not None:
            for comunidad, provincia, votos, diputados in datos_resultados:
                # 1. Comprobamos si la comunidad ya existe en nuestro diccionario principal
                # Si no existe, le creamos un diccionario vacío para meter sus provincias
                if comunidad not in self.resultados_por_comunidad:
                    self.resultados_por_comunidad[comunidad] = {}
                
                # 2. Guardamos la tupla (votos, diputados) en la provincia y comunidad correspondientes
                self.resultados_por_comunidad[comunidad][provincia] = (votos, diputados)



    @property
    def num_provincias_presentado(self):
        """
        Propiedad derivada: Calcula en cuántas provincias en total 
        se ha presentado este partido.
        """
        total_provincias = 0
        # Recorremos los diccionarios de provincias de cada comunidad
        for provincias_comunidad in self.resultados_por_comunidad.values():
            # Sumamos la cantidad de provincias (la longitud del diccionario)
            total_provincias += len(provincias_comunidad)
            
        return total_provincias