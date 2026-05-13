from abc import ABC, abstractmethod
from registro import RegistroClasificacion, RegistroRegresion
import math

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

    def calcular_medias_desviaciones(self):
        """
        Calcula la media y la desviación típica para cada columna de atributos.
        """
        if not self.registros:
            return [], []

        n = len(self.registros)
        matriz = [registro.atributos for registro in self.registros]
        
        medias = []
        desviaciones = []
        
        num_columnas = len(self.nombres_atributos)
        for i in range(num_columnas):
            columna = [fila[i] for fila in matriz]
            media = sum(columna) / n
            varianza = sum((x - media)**2 for x in columna) / n
            desviacion = math.sqrt(varianza)
            
            medias.append(media)
            desviaciones.append(desviacion)
            
        return medias, desviaciones

    def clonar_con_nuevos_atributos(self, lista_nuevos_atributos):
        """
        Crea un nuevo DataSet del mismo tipo que el actual, pero sustituyendo 
        los atributos de cada registro por los proporcionados en la lista.
        """
        if len(lista_nuevos_atributos) != len(self.registros):
            raise ValueError("La lista de nuevos atributos debe tener el mismo tamaño que el número de registros.")

        # Creamos una instancia de la misma clase (DataSetClasificacion o Regresion)
        nuevo_dataset = type(self)()
        nuevo_dataset.nombres_atributos = self.nombres_atributos.copy()

        for reg, nuevos_atribs in zip(self.registros, lista_nuevos_atributos):
            # Creamos un nuevo registro del mismo tipo pasándole la nueva lista
            nuevo_registro = type(reg)(nuevos_atribs, reg.objetivo)
            
            # Lo añadimos al nuevo DataSet
            nuevo_dataset.agregar_registro(nuevo_registro)
            
        return nuevo_dataset
    

class DataSetClasificacion(DataSet):
    def agregar_registro(self, registro):
        """
        Implementación concreta para clasificación.
        Solo permite añadir objetos que sean instancia de RegistroClasificacion.
        """
        if isinstance(registro, RegistroClasificacion):
            self.registros.append(registro)
        else:
            raise TypeError("Error: El registro debe ser de tipo RegistroClasificacion.")

class DataSetRegresion(DataSet):
    def agregar_registro(self, registro):
        """
        Implementación concreta para regresión.
        Solo permite añadir objetos que sean instancia de RegistroRegresion.
        """
        if isinstance(registro, RegistroRegresion):
            self.registros.append(registro)
        else:
            raise TypeError("Error: El registro debe ser de tipo RegistroRegresion.")

    def calcular_correlaciones(self):
        """
        Calcula el valor absoluto de la correlación de Pearson entre cada 
        lag (atributo) y el objetivo. Se usa como pesos para kNN.
        """
        n = len(self.registros)
        if n < 2:
            return [1.0] * len(self.nombres_atributos)

        y = [reg.objetivo for reg in self.registros]
        media_y = sum(y) / n
        ss_y = sum((val - media_y)**2 for val in y)

        pesos = []
        for i in range(len(self.nombres_atributos)):
            x_i = [reg.atributos[i] for reg in self.registros]
            media_x = sum(x_i) / n
            ss_x = sum((val - media_x)**2 for val in x_i)
            
            cov_xy = sum((x_i[j] - media_x) * (y[j] - media_y) for j in range(n))
            
            if ss_x == 0 or ss_y == 0:
                r = 0.0
            else:
                r = cov_xy / math.sqrt(ss_x * ss_y)
            
            # Usamos valor absoluto porque una correlación negativa fuerte es igual de informativa
            pesos.append(abs(r))
            
        return pesos