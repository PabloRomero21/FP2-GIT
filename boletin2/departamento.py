# departamento.py

class Departamento:
    """Clase de dominio que representa un departamento de la Universidad."""
    
    def __init__(self, nombre: str, numero_etc: float, prof_tc: float, prof_tp: float, experimentalidad: float):
        self.nombre = nombre
        self.numero_etc = numero_etc
        self.prof_tc = prof_tc
        self.prof_tp = prof_tp
        self.experimentalidad = experimentalidad

    @property
    def total_profesores(self) -> float:
        """Calcula el total de profesores en tiempo real."""
        return self.prof_tc + (0.5 * self.prof_tp)

    @property
    def carga_docente_real(self) -> float:
        """Calcula la carga docente en tiempo real."""
        if self.total_profesores == 0:
            return float('inf') 
        return (self.numero_etc * self.experimentalidad) / self.total_profesores

    def es_integro(self, total_pdf: float) -> bool:
        """Devuelve True si el cálculo coincide con el PDF, False si no."""
        return round(self.total_profesores, 2) == round(total_pdf, 2)

    def __str__(self) -> str:
        carga_str = "Infinita" if self.carga_docente_real == float('inf') else f"{self.carga_docente_real:.2f}"
        return f"Depto: {self.nombre:<75} | Total Prof: {self.total_profesores:<6} | Carga Real: {carga_str}"