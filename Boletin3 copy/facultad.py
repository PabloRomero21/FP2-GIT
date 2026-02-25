# facultad.py
from departamento import Departamento

class Facultad:
    """Clase que representa un centro o facultad. Contiene departamentos."""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._departamentos = []

    def agregar_departamento(self, departamento: Departamento):
        """Añade un departamento a la facultad."""
        if isinstance(departamento, Departamento):
            self._departamentos.append(departamento)
        else:
            raise TypeError("Solo se pueden añadir objetos Departamento.")

    def obtener_extremos_carga(self) -> tuple:
        """Devuelve una tupla con (Depto_Mayor_Carga, Depto_Menor_Carga)."""
        if not self._departamentos:
            return None, None
            
        depto_mayor = max(self._departamentos, key=lambda d: d.carga_docente_real)
        depto_menor = min(self._departamentos, key=lambda d: d.carga_docente_real)
        
        return depto_mayor, depto_menor

    def __str__(self) -> str:
        resultado = f"=== SEDE: {self.nombre} ===\n"
        if not self._departamentos:
            resultado += "  [!] No hay departamentos asignados a esta facultad.\n"
        else:
            for depto in self._departamentos:
                resultado += f"    - {depto.nombre}\n"
        return resultado
    
    def top_n_mayor_carga(self, n: int) -> list:
        return sorted(self._departamentos, key=lambda d: d.carga_docente_real, reverse=True)[:n]

    def top_n_menor_carga(self, n: int) -> list:
        return sorted(self._departamentos, key=lambda d: d.carga_docente_real)[:n]

    def contar_por_experimentalidad(self) -> dict:
        conteo = {}
        for depto in self._departamentos:
            coef = depto.experimentalidad
            conteo[coef] = conteo.get(coef, 0) + 1
        return conteo

    def media_carga_por_experimentalidad(self) -> dict:
        suma_cargas = {}
        conteo = self.contar_por_experimentalidad()
        
        for depto in self._departamentos:
            coef = depto.experimentalidad
            if depto.carga_docente_real != float('inf'):
                suma_cargas[coef] = suma_cargas.get(coef, 0.0) + depto.carga_docente_real
            
        return {coef: suma_cargas[coef] / conteo[coef] for coef in suma_cargas}

    def extremos_media_experimentalidad(self) -> tuple:
        medias = self.media_carga_por_experimentalidad()
        if not medias:
            return None, None
            
        coef_mayor = max(medias, key=medias.get)
        coef_menor = min(medias, key=medias.get)
        return coef_mayor, coef_menor