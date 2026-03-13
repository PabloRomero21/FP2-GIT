from abc import ABC, abstractmethod
from registro import RegistroClasificacion, RegistroRegresion

class DataSet(ABC):
    def __init__(self):
        """
        Constructor de la clase abstracta DataSet.
        Inicializa las listas vacías para almacenar los registros y los nombres de los atributos.
        """
        self.registros = []
        self.nombres_atributos = []

    def set_cabeceras(self, lista_str):
        """
        Recibe una lista de cadenas de texto y asigna todos los elementos, 
        excepto el último, a la lista de nombres_atributos.
        """
        if lista_str:
            self.nombres_atributos = lista_str[:-1]

    @abstractmethod
    def agregar_registro(self, registro):
        """
        Método abstracto. Fuerza a las clases hijas a implementar la lógica 
        para añadir un objeto 'registro' a la lista 'self.registros'.
        """
        pass

    def calcular_min_max(self):
        """
        Calcula y devuelve dos listas con los valores mínimos y máximos 
        para cada índice de atributos en los registros del DataSet.
        """
        if not self.registros:
            return [], []

        matriz_atributos = [registro.atributos for registro in self.registros]
        minimos = [min(columna) for columna in zip(*matriz_atributos)]
        maximos = [max(columna) for columna in zip(*matriz_atributos)]

        return minimos, maximos

    def crear_subconjunto(self, lista_registros):
        """
        Recibe una lista de objetos Registro y devuelve un nuevo objeto DataSet 
        (de la misma clase hija) con esos registros y los mismos nombres de atributos.
        """
        # 1. Instanciamos dinámicamente la clase hija correcta (Polimorfismo)
        nuevo_dataset = self.__class__()
        
        # 2. Asignamos la nueva lista de registros pasada como argumento
        nuevo_dataset.registros = lista_registros
        
        # 3. Copiamos los nombres de los atributos del objeto actual
        # Usamos .copy() para evitar que ambos datasets modifiquen la misma lista por accidente
        nuevo_dataset.nombres_atributos = self.nombres_atributos.copy()
        
        return nuevo_dataset
    
    def calcular_medias_desviaciones(self):
        """
        Calcula y devuelve dos listas: las medias y las desviaciones típicas 
        para cada columna de atributos en los registros del DataSet.
        """
        if not self.registros:
            return [], []

        # Extraemos las columnas como hicimos en el min_max
        matriz_atributos = [registro.atributos for registro in self.registros]
        columnas = list(zip(*matriz_atributos))
        
        medias = []
        desviaciones = []
        n = len(self.registros)
        
        import math # Por si no lo has importado arriba del todo
        
        for col in columnas:
            # 1. Calcular la Media
            media = sum(col) / n
            medias.append(media)
            
            # 2. Calcular la Desviación Típica (Poblacional)
            varianza = sum((x - media) ** 2 for x in col) / n
            desviaciones.append(math.sqrt(varianza))
            
        return medias, desviaciones
    
    def eliminar_atributos(self, indices_a_eliminar):
        """
        Recibe una lista o conjunto de índices. Devuelve un NUEVO DataSet 
        del mismo tipo, excluyendo las columnas correspondientes a esos índices.
        """
        # 1. Comprobar que hay datos y definir el límite lógico
        if not self.registros:
            raise ValueError("El DataSet está vacío, no se pueden eliminar atributos.")
            
        # El número de atributos lógicos lo marca la longitud de la lista de atributos del primer registro
        num_atributos = len(self.registros[0].atributos)
        
        # 2. VALIDACIÓN: Comprobar que todos los índices están en el rango correcto
        for idx in indices_a_eliminar:
            if idx < 0 or idx >= num_atributos:
                raise ValueError(f"Error: El índice {idx} está fuera de rango. Debe estar entre 0 y {num_atributos - 1}.")

        # 3. Instanciamos el nuevo DataSet dinámicamente (Polimorfismo)
        nuevo_dataset = self.__class__()
        
        # 4. Filtrar los nombres de los atributos (cabeceras) si las hay
        if self.nombres_atributos:
            nuevos_nombres = []
            for i, nombre in enumerate(self.nombres_atributos):
                if i not in indices_a_eliminar:
                    nuevos_nombres.append(nombre)
            nuevo_dataset.nombres_atributos = nuevos_nombres

        # 5. Filtrar y clonar los registros
        for reg in self.registros:
            # Filtramos la lista de números del registro actual
            nuevos_atributos = []
            for i, valor in enumerate(reg.atributos):
                if i not in indices_a_eliminar:
                    nuevos_atributos.append(valor)
                    
            # Instanciamos un nuevo Registro del mismo tipo (Clasificación o Regresión)
            # type(reg) averigua la clase exacta y llama a su constructor pasándole la nueva lista
            nuevo_registro = type(reg)(nuevos_atributos, reg.objetivo)
            
            # Lo añadimos al nuevo DataSet
            nuevo_dataset.agregar_registro(nuevo_registro)
            
        return nuevo_dataset
    

class DataSetClasificacion(DataSet):
    def agregar_registro(self, registro):
        """
        Implementación concreta para clasificación.
        Solo permite añadir objetos que sean instancia de RegistroClasificacion.
        """
        # Comprobamos si el objeto 'registro' es de la clase 'RegistroClasificacion'
        if isinstance(registro, RegistroClasificacion):
            self.registros.append(registro)
        else:
            # Si intentan meter un registro incorrecto (ej. Regresion o un string), lanzamos error
            raise TypeError("Error: El registro debe ser de tipo RegistroClasificacion.")

class DataSetRegresion(DataSet):
    def agregar_registro(self, registro):
        """
        Implementación concreta para regresión.
        Solo permite añadir objetos que sean instancia de RegistroRegresion.
        """
        # Comprobamos si el objeto 'registro' es de la clase 'RegistroRegresion'
        if isinstance(registro, RegistroRegresion):
            self.registros.append(registro)
        else:
            # Protegemos la integridad de los datos lanzando un error si no coincide
            raise TypeError("Error: El registro debe ser de tipo RegistroRegresion.")