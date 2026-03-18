from estadistica import Estadistica


class Jugador:
    """
    Representa a un jugador en un equipo concreto durante una temporada concreta.
    Equivale a una fila del fichero Excel, pero encapsulada con sus propiedades derivadas.
    Delega los datos estadísticos brutos a un objeto Estadistica (composición).
    """

    def __init__(self, nombre: str, estadistica: Estadistica):
        self.nombre = nombre
        self.estadistica = estadistica  # Objeto Estadistica que contiene los datos de esa temporada

    # -------------------------------------------------------------------------
    # PROPIEDADES DERIVADAS
    # -------------------------------------------------------------------------

    @property
    def tarjetas_totales(self) -> int:
        """
        Total de sanciones disciplinarias: tarjetas amarillas más expulsiones directas.
        """
        return int(self.estadistica.tarjetas + self.estadistica.expulsiones)

    @property
    def veces_sustituido(self) -> int:
        """
        Veces que el jugador fue sustituido: partidos como titular menos partidos completados.
        Si empezó 10 partidos pero solo acabó 7, fue sustituido en 3.
        """
        return int(self.estadistica.ptitular - self.estadistica.pcompletos)

    @property
    def goles_por_minuto(self) -> float:
        """
        Eficiencia goleadora: goles dividido entre minutos jugados.
        Devuelve 0.0 si no ha jugado ningún minuto para evitar división por cero.
        """
        if self.estadistica.minutos > 0:
            return round(self.estadistica.goles / self.estadistica.minutos, 6)
        return 0.0

    @property
    def es_revulsivo(self) -> bool:
        """
        Un jugador es revulsivo si jugó más partidos saliendo desde el banquillo
        (suplente) que como titular.
        """
        return self.estadistica.psuplente > self.estadistica.ptitular

    # -------------------------------------------------------------------------

    def __str__(self):
        return (f"Jugador: {self.nombre} | "
                f"Temporada: {self.estadistica.temporada} | "
                f"Equipo: {self.estadistica.equipo} | "
                f"Goles: {int(self.estadistica.goles)} | "
                f"Revulsivo: {self.es_revulsivo}")
