class Provincia:
    def __init__(self, nombre, poblacion, numero_de_mesas, censo_electoral_sin_cera, 
                 censo_cera, total_censo_electoral, total_votantes_cer, 
                 total_votantes_cera, total_votantes, votos_validos, 
                 votos_a_candidaturas, votos_en_blanco, votos_en_nulo, 
                 lista_partidos=None):  # <-- Ahora recibimos una lista
        
        # Atributos básicos
        self.nombre = nombre
        self.poblacion = poblacion
        self.numero_de_mesas = numero_de_mesas
        self.censo_electoral_sin_cera = censo_electoral_sin_cera
        self.censo_cera = censo_cera
        self.total_censo_electoral = total_censo_electoral
        self.total_votantes_cer = total_votantes_cer
        self.total_votantes_cera = total_votantes_cera
        self.total_votantes = total_votantes
        self.votos_validos = votos_validos
        self.votos_a_candidaturas = votos_a_candidaturas
        self.votos_en_blanco = votos_en_blanco
        self.votos_en_nulo = votos_en_nulo
        
        # Inicializamos el diccionario vacío
        self.resultados_partidos = {}
        
        # Si nos han pasado una lista, la transformamos a nuestro diccionario
        if lista_partidos is not None:
            for nombre_partido, votos, diputados in lista_partidos:
                # La clave es el nombre, el valor es la tupla (votos, diputados)
                self.resultados_partidos[nombre_partido] = (votos, diputados)

    @property
    def porcentaje_nulos_blancos(self):
        """Propiedad derivada: Calcula el % de votos nulos y en blanco sobre el total de votantes."""
        votos_invalidos = self.votos_en_blanco + self.votos_en_nulo
        
        # Evitamos el error de división por cero por si hay datos corruptos
        if self.total_votantes == 0:
            return 0.0
            
        return (votos_invalidos / self.total_votantes) * 100
    

    @property
    def participacion_cera(self):
        """Calcula el % de participación de los residentes ausentes (CERA)."""
        # Evitamos la división por cero si en alguna provincia no hay censo CERA
        if self.censo_cera == 0:
            return 0.0
            
        return (self.total_votantes_cera / self.censo_cera) * 100