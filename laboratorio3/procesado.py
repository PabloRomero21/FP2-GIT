from abc import ABC, abstractmethod

class Preprocesamiento(ABC):
    """
    Clase abstracta que define la interfaz para cualquier técnica de 
    preprocesado de datos (normalización, selección de atributos, etc.).
    """

    @abstractmethod
    def ajustar(self, dataset):
        """
        Calcula los parámetros necesarios para la transformación 
        a partir de un objeto DataSet.
        """
        pass

    @abstractmethod
    def transformar_dataSet(self, dataset):
        """
        Aplica la transformación a todo un DataSet y devuelve uno nuevo.
        """
        pass

    @abstractmethod
    def transformar_registro(self, registro):
        """
        Aplica la transformación a un único objeto Registro y devuelve uno nuevo.
        """
        pass