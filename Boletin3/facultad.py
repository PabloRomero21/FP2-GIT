from departamento import Departamento

class Facultad:
    """Clase de dominio que representa un centro o facultad de la Universidad."""
    
    def __init__(self, nombre: str):
        # 1. Validación básica para la consistencia de los datos
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre de la facultad debe ser un texto válido y no vacío.")
            
        self.nombre = nombre.strip()
        
        # 2. Encapsulamiento: La lista se define como protegida (con un guion bajo)
        # para evitar que desde fuera de la clase se modifique la lista directamente.
        self._departamentos = []

    def agregar_departamento(self, departamento: Departamento):
        """Método de acceso para añadir departamentos de forma segura."""
        # Verificamos que lo que se inserta es estrictamente un objeto Departamento
        if isinstance(departamento, Departamento):
            self._departamentos.append(departamento)
        else:
            raise TypeError("El objeto a insertar debe ser de la clase Departamento.")

    def __str__(self) -> str:
        """
        Método mágico para representar el objeto como una cadena de texto.
        Muestra el nombre de la facultad y lista sus departamentos.
        """
        # Cabecera con el nombre de la Facultad
        resultado = f"=== {self.nombre} ===\n"
        
        # Comprobamos si la lista está vacía
        if not self._departamentos:
            resultado += "  [!] No hay departamentos asignados a esta facultad.\n"
        else:
            resultado += "  Departamentos asignados:\n"
            # Iteramos sobre la lista para imprimir el nombre de cada departamento
            for depto in self._departamentos:
                resultado += f"    - {depto.nombre}\n"
                
        return resultado
    
    def obtener_extremos_carga(self) -> tuple:
        """
        Devuelve una tupla con los departamentos que tienen la mayor y menor 
        carga docente de esta facultad.
        Retorna: (Departamento_MAYOR_carga, Departamento_MENOR_carga)
        """
        # 1. Protección de seguridad: si la facultad no tiene departamentos, no podemos calcular nada.
        if not self._departamentos:
            return None, None
            
        # 2. Usamos max() y min() delegando la comparación a la función lambda
        # Esto busca en la lista interna de la clase de forma ultra eficiente
        depto_mayor = max(self._departamentos, key=lambda d: d.carga_docente_real)
        depto_menor = min(self._departamentos, key=lambda d: d.carga_docente_real)
        
        # 3. Retornamos la tupla inmutable con ambos objetos
        return (depto_mayor, depto_menor)