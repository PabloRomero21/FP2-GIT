# departamento.py

class Departamento:
    """Clase de dominio que representa un departamento de la Universidad."""
    
    def __init__(self, nombre: str, numero_etc: float, prof_tc: float, prof_tp: float, experimentalidad: float):
        
        # 1. Validar el Nombre
        if not isinstance(nombre, str):
            raise TypeError("El nombre del departamento debe ser un texto (string).")
        if not nombre.strip():
            raise ValueError("El nombre del departamento no puede estar vacío.")
            
        # 2. Validar Profesores (No pueden ser negativos)
        if prof_tc < 0 or prof_tp < 0:
            raise ValueError(f"Los profesores no pueden ser negativos. Datos recibidos: TC={prof_tc}, TP={prof_tp}")
            
        # 3. Validar Número ETC
        if numero_etc < 0:
            raise ValueError(f"El número ETC no puede ser negativo. Recibido: {numero_etc}")
            
        # 4. Validar Experimentalidad (Debe ser estrictamente mayor que cero)
        if experimentalidad <= 0:
            raise ValueError(f"El coeficiente de experimentalidad debe ser mayor que 0. Recibido: {experimentalidad}")

        # Si supera todas las barreras de seguridad, guardamos los datos
        self.nombre = nombre.strip()  # Guardamos el nombre limpio de espacios extra
        self.numero_etc = float(numero_etc)
        self.prof_tc = float(prof_tc)
        self.prof_tp = float(prof_tp)
        self.experimentalidad = float(experimentalidad)
        self.sede = None

        
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