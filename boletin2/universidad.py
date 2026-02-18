# universidad.py
from departamento import Departamento

class Universidad:
    """Clase que gestiona la colección de departamentos y la lógica de negocio."""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.departamentos = []

    def agregar_departamento(self, departamento: Departamento):
        if isinstance(departamento, Departamento):
            self.departamentos.append(departamento)
        else:
            raise TypeError("El objeto a insertar debe ser de la clase Departamento")

    def top_n_mayor_carga(self, n: int) -> list:
        return sorted(self.departamentos, key=lambda d: d.carga_docente_real, reverse=True)[:n]

    def top_n_menor_carga(self, n: int) -> list:
        return sorted(self.departamentos, key=lambda d: d.carga_docente_real)[:n]

    def contar_por_experimentalidad(self) -> dict:
        conteo = {}
        for depto in self.departamentos:
            coef = depto.experimentalidad
            conteo[coef] = conteo.get(coef, 0) + 1
        return conteo

    def media_carga_por_experimentalidad(self) -> dict:
        suma_cargas = {}
        conteo = self.contar_por_experimentalidad()
        
        for depto in self.departamentos:
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