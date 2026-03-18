class Estadistica:
    """
    Representa el rendimiento de un jugador en un equipo durante una temporada concreta.
    (Equivale a una fila del archivo Excel)
    """
    def __init__(self, temporada: str, equipo: str, pjugados: float, pcompletos: float,
                 ptitular: float, psuplente: float, minutos: float, lesiones: float,
                 tarjetas: float, expulsiones: float, goles: float, penalties_fallados: float):
        self.temporada = temporada
        self.equipo = equipo
        self.pjugados = pjugados
        self.pcompletos = pcompletos
        self.ptitular = ptitular
        self.psuplente = psuplente
        self.minutos = minutos
        self.lesiones = lesiones
        self.tarjetas = tarjetas
        self.expulsiones = expulsiones
        self.goles = goles
        self.penalties_fallados = penalties_fallados

    def __str__(self):
        return f"[{self.temporada} | {self.equipo}] Partidos: {self.pjugados} - Goles: {self.goles}"