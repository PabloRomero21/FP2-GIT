from estadistica import Estadistica

class Jugador:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.estadisticas = []  # Ahora es una lista de OBJETOS Estadistica

    def agregar_estadisticas(self, temporada: str, equipo: str, pjugados: float, pcompletos: float,
                             ptitular: float, psuplente: float, minutos: float, lesiones: float,
                             tarjetas: float, expulsiones: float, goles: float, penalties_fallados: float):
        
        
        """Crea un objeto Estadistica y lo añade a la lista del jugador."""
        nueva_est = Estadistica(temporada, equipo, pjugados, pcompletos, ptitular, psuplente, 
                                minutos, lesiones, tarjetas, expulsiones, goles, penalties_fallados)
        self.estadisticas.append(nueva_est)

    def __str__(self):
        return f"Jugador: {self.nombre} ({len(self.estadisticas)} registros de temporada)"