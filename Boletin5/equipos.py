class Equipo:
    """
    Representa a un club de fútbol en una temporada concreta.
    Contiene la lista de jugadores que militaron en él ese año, junto con sus estadísticas.
    Cada instancia de Equipo corresponde exactamente a una (temporada, club) del Excel.
    """

    def __init__(self, nombre: str, temporada_id: str):
        self.nombre = nombre
        self.temporada_id = temporada_id      # Identificador de la temporada a la que pertenece
        self.jugadores = []                   # Lista de objetos Jugador (uno por fila del Excel)

    # -------------------------------------------------------------------------
    # MÉTODO DE INSERCIÓN
    # -------------------------------------------------------------------------

    def agregar_jugador(self, jugador):
        """
        Añade un objeto Jugador a la plantilla del equipo en esta temporada.
        """
        self.jugadores.append(jugador)

    # -------------------------------------------------------------------------
    # PROPIEDADES DERIVADAS
    # -------------------------------------------------------------------------

    @property
    def goles_marcados(self) -> float:
        """
        Suma de los goles marcados por todos los jugadores del equipo en esta temporada.
        """
        return sum(j.estadistica.goles for j in self.jugadores)

    @property
    def num_jugadores(self) -> int:
        """
        Número de jugadores registrados en el equipo durante esta temporada.
        """
        return len(self.jugadores)

    @property
    def partidos_jugados(self) -> float:
        """
        Suma de los partidos jugados por todos los jugadores del equipo en esta temporada.
        """
        return sum(j.estadistica.pjugados for j in self.jugadores)

    @property
    def total_tarjetas(self) -> int:
        """
        Suma del total de sanciones disciplinarias (tarjetas + expulsiones) de todo el equipo
        en esta temporada. Delega en la propiedad derivada tarjetas_totales de cada Jugador.
        """
        return sum(j.tarjetas_totales for j in self.jugadores)

    # -------------------------------------------------------------------------

    def __str__(self):
        return (f"Equipo: {self.nombre} | "
                f"Temporada: {self.temporada_id} | "
                f"Jugadores: {self.num_jugadores} | "
                f"Goles: {int(self.goles_marcados)}")
