from abc import ABC, abstractmethod

# Opcional pero recomendado: importamos DataSet para dar pistas de tipado (Type Hinting)
# from dataset import DataSet

class Modelo(ABC):
    def __init__(self):
        """
        Constructor de la clase abstracta Modelo.
        Inicializa el atributo datos_entrenamiento a nulo (None en Python).
        """
        self.datos_entrenamiento = None

    def entrenar(self, dataset):
        """
        Recibe un objeto DataSet y lo guarda en el atributo de entrenamiento.
        Este es el paso donde la IA "memoriza" o "aprende" de los datos.
        """
        self.datos_entrenamiento = dataset

    @abstractmethod
    def predecir(self, registro):
        """
        Método abstracto.
        Recibe un objeto Registro y debe devolver la predicción (una clase o un valor real).
        Como cada algoritmo predice de forma diferente, obligamos a las clases hijas a implementarlo.
        """
        pass