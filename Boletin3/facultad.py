from universidad import Universidad
from departamento import Departamento

class Facultad(Universidad):
    """
    Clase que representa un centro o facultad.
    Hereda de Universidad para reutilizar toda la lógica de análisis de departamentos.
    """
    
    def __init__(self, nombre: str):
        # 1. Llamamos al constructor de la clase Padre (Universidad).
        # Esto automáticamente crea self.nombre y la lista vacía self._departamentos,
        # además de heredar métodos como agregar_departamento, top_n_mayor_carga, etc.
        super().__init__(nombre)

    # 2. Polimorfismo / Sobrescritura (Overriding):
    # Reescribimos el método mágico __str__ para que al imprimir una Facultad
    # se vea distinto a como se imprimiría una Universidad.
    def __str__(self) -> str:
        """Muestra el nombre de la facultad y lista sus departamentos de forma visual."""
        resultado = f"=== SEDE: {self.nombre} ===\n"
        
        if not self._departamentos:
            resultado += "  [!] No hay departamentos asignados a esta facultad.\n"
        else:
            resultado += "  Departamentos asignados:\n"
            for depto in self._departamentos:
                resultado += f"    - {depto.nombre}\n"
                
        return resultado
    
    def obtener_extremos_carga(self) -> tuple:
            """Devuelve una tupla con (Depto_Mayor_Carga, Depto_Menor_Carga)."""
            if not self._departamentos:
                return None, None
                
            depto_mayor = max(self._departamentos, key=lambda d: d.carga_docente_real)
            depto_menor = min(self._departamentos, key=lambda d: d.carga_docente_real)
            
            return depto_mayor, depto_menor