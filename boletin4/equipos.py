class Equipo:
    """
    Representa un club de fútbol.
    Agrupa a los jugadores que han pasado por él organizados por temporadas.
    """
    def __init__(self, nombre: str):
        self.nombre = nombre
        # Diccionario -> Clave: str (temporada) | Valor: list (lista de tuplas (Jugador, Estadistica))
        self.temporadas = {}

    def agregar_registro(self, temporada: str, jugador_obj, estadistica_obj):
        """
        Añade un jugador y sus estadísticas a una temporada específica del equipo.
        """
        # Si es la primera vez que registramos esta temporada, creamos una lista vacía
        if temporada not in self.temporadas:
            self.temporadas[temporada] = []
            
        # Añadimos la tupla a la lista de esa temporada
        self.temporadas[temporada].append((jugador_obj, estadistica_obj))

    def __str__(self):
        return f"Equipo: {self.nombre} ({len(self.temporadas)} temporadas registradas)"