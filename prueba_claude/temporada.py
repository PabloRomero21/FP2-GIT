class Temporada:
    """
    Representa una temporada de La Liga.
    Agrupa todos los equipos que participaron en ella, indexados por nombre de club.
    Su identificador sigue el formato XXXX-YY (ej: '2017-18').
    """

    def __init__(self, id_temporada: str):
        self.id_temporada = id_temporada
        # Diccionario -> Clave: str (nombre del equipo) | Valor: Equipo
        self.equipos = {}

    # -------------------------------------------------------------------------
    # MÉTODO DE INSERCIÓN
    # -------------------------------------------------------------------------

    def agregar_equipo(self, equipo):
        """
        Registra un objeto Equipo en el diccionario de equipos de esta temporada.
        La clave es el nombre del club.
        """
        self.equipos[equipo.nombre] = equipo

    # -------------------------------------------------------------------------
    # PROPIEDADES DERIVADAS
    # -------------------------------------------------------------------------

    @property
    def num_equipos(self) -> int:
        """
        Número de equipos que participaron en esta temporada.
        """
        return len(self.equipos)

    @property
    def num_partidos(self) -> int:
        """
        Número total de partidos de la temporada en un formato de liga todos contra todos
        (ida y vuelta): N * (N - 1).
        Si hay menos de 2 equipos, no se puede celebrar ningún partido.
        """
        n = self.num_equipos
        if n < 2:
            return 0
        return n * (n - 1)

    @property
    def goles_totales(self) -> float:
        """
        Suma de los goles marcados por todos los equipos en esta temporada.
        """
        return sum(eq.goles_marcados for eq in self.equipos.values())

    @property
    def media_goles_por_partido(self) -> float:
        """
        Promedio de goles por partido en esta temporada.
        Devuelve 0.0 si no hay partidos registrados.
        """
        if self.num_partidos > 0:
            return round(self.goles_totales / self.num_partidos, 4)
        return 0.0

    @property
    def año_inicio(self) -> int:
        """
        Extrae el año de inicio de la temporada a partir de su identificador.
        Ejemplo: '2017-18' -> 2017.
        """
        try:
            return int(str(self.id_temporada).split('-')[0])
        except (ValueError, AttributeError):
            return 0

    # -------------------------------------------------------------------------

    def __str__(self):
        return (f"Temporada: {self.id_temporada} | "
                f"Equipos: {self.num_equipos} | "
                f"Partidos: {self.num_partidos} | "
                f"Goles: {int(self.goles_totales)} | "
                f"Media: {self.media_goles_por_partido:.2f} goles/partido")
