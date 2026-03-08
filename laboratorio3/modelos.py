from abc import ABC, abstractmethod
from collections import Counter

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


class Clasificador_kNN(Modelo):
    def __init__(self, k, distancia="euclídea", pesos=None):
        """
        Constructor del clasificador kNN.
        Hereda de Modelo y configura los hiperparámetros del algoritmo.
        """
        # Invocamos al constructor padre para que inicialice self.datos_entrenamiento
        super().__init__() 
        
        self.k = k
        self.distancia = distancia
        self.pesos = pesos

    def predecir(self, registro_test):
        """
        Predice la etiqueta de un nuevo registro evaluando la distancia a los
        registros de entrenamiento y haciendo una votación entre los k más cercanos.
        """
        # 1. Seguridad: Verificar que el modelo haya sido entrenado primero
        if self.datos_entrenamiento is None or not self.datos_entrenamiento.registros:
            raise ValueError("Error: El modelo no está entrenado o el dataset está vacío.")

        # Extraemos la lista pura de registros de nuestro contenedor DataSet
        registros_train = self.datos_entrenamiento.registros

        # 2. Búsqueda de vecinos
        # El método k_vecinos está en la clase Registro, así que el 'registro_test' lo invoca.
        # Nos devolverá una lista con los ÍNDICES de los registros más cercanos.
        indices_vecinos = registro_test.k_vecinos(
            registros_train, 
            self.k, 
            tipo=self.distancia, 
            pesos=self.pesos
        )

        # 3. Recopilar los 'votos' (las etiquetas objetivo de esos vecinos)
        etiquetas_vecinos = []
        for indice in indices_vecinos:
            # Accedemos al registro de entrenamiento por su índice y extraemos su objetivo
            vecino = registros_train[indice]
            etiquetas_vecinos.append(vecino.objetivo)

        # 4. Encontrar la etiqueta más común (la moda)
        # Counter crea un diccionario con las frecuencias: {'Iris-setosa': 3, 'Iris-versicolor': 2}
        contador = Counter(etiquetas_vecinos)
        
        # most_common(1) devuelve una lista con una tupla del más común: [('Iris-setosa', 3)]
        # Con [0][0] extraemos directamente el texto de la etiqueta ganadora
        etiqueta_ganadora = contador.most_common(1)[0][0]

        return etiqueta_ganadora
    
class Regresor_kNN(Modelo):
    def __init__(self, k, distancia="euclídea", pesos=None):
        """
        Constructor del regresor kNN.
        Hereda de Modelo y configura los hiperparámetros.
        """
        super().__init__() 
        self.k = k
        self.distancia = distancia
        self.pesos = pesos

    def predecir(self, registro_test):
        """
        Predice el valor continuo de un nuevo registro calculando la 
        media matemática de los valores de sus k vecinos más cercanos.
        """
        # 1. Seguridad: Verificar que el modelo haya sido entrenado
        if self.datos_entrenamiento is None or not self.datos_entrenamiento.registros:
            raise ValueError("Error: El modelo no está entrenado o el dataset está vacío.")

        registros_train = self.datos_entrenamiento.registros

        # 2. Búsqueda de vecinos (Reutilizamos la inteligencia espacial de Registro)
        indices_vecinos = registro_test.k_vecinos(
            registros_train, 
            self.k, 
            tipo=self.distancia, 
            pesos=self.pesos
        )

        # 3. Recopilar los valores (precios, medidas, etc.) de esos vecinos
        valores_vecinos = []
        for indice in indices_vecinos:
            vecino = registros_train[indice]
            # Como la factoría creó RegistrosRegresion, sabemos que esto es un float numérico
            valores_vecinos.append(vecino.objetivo)

        # 4. Calcular la media matemática
        # Sumamos todos los valores y dividimos entre la cantidad de vecinos (k)
        prediccion_valor = sum(valores_vecinos) / len(valores_vecinos)

        return prediccion_valor