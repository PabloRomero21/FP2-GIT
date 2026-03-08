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
        
        return 
    

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