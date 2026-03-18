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
    """
    Regresor basado en los k vecinos más cercanos.
    """
    def __init__(self, k, distancia="euclídea"):
        super().__init__() 
        self.k = k
        self.distancia = distancia

    def predecir(self, registro_test):
        if self.datos_entrenamiento is None or not self.datos_entrenamiento.registros:
            raise ValueError("El modelo no está entrenado.")

        registros_train = self.datos_entrenamiento.registros

        # Invocamos k_vecinos desde el registro que nos pasan
        indices_vecinos = registro_test.k_vecinos(
            registros_train, 
            self.k, 
            tipo=self.distancia
        )

        # Recopilamos los valores reales de esos vecinos
        valores_vecinos = []
        for indice in indices_vecinos:
            valores_vecinos.append(registros_train[indice].objetivo)

        # Devolvemos la media matemática
        return sum(valores_vecinos) / len(valores_vecinos)
    
class Clasificador_centroide(Modelo):
    """
    Clasificador que calcula un prototipo (centroide) para cada etiqueta
    y predice la etiqueta del centroide más cercano.
    """
    def __init__(self, distancia="euclídea"):
        super().__init__()
        self.distancia = distancia
        self.centroides = {} # Diccionario: { 'Iris-setosa': objeto_registro_centroide }

    def entrenar(self, dataset):
        """Calcula y almacena el centroide de cada clase."""
        super().entrenar(dataset)
        
        # 1. Agrupar los registros por etiqueta
        grupos = {}
        for reg in dataset.registros:
            etiqueta = reg.objetivo
            if etiqueta not in grupos:
                grupos[etiqueta] = []
            grupos[etiqueta].append(reg.atributos)

        # 2. Calcular la media de cada atributo para cada etiqueta
        for etiqueta, lista_atributos in grupos.items():
            n = len(lista_atributos)
            num_atributos = len(lista_atributos[0])
            atributos_centroide = []
            
            for i in range(num_atributos):
                # Sumamos el atributo 'i' de todos los registros de esta clase
                suma = sum(atributos[i] for atributos in lista_atributos)
                atributos_centroide.append(suma / n)

            # 3. Guardamos el centroide como un objeto RegistroClasificacion
            from registro import RegistroClasificacion
            self.centroides[etiqueta] = RegistroClasificacion(atributos_centroide, etiqueta)

    def predecir(self, registro_test):
        """Busca y devuelve la etiqueta del centroide más cercano."""
        if not self.centroides:
            raise ValueError("El modelo no está entrenado.")

        mejor_etiqueta = None
        menor_distancia = float('inf')

        for etiqueta, centroide in self.centroides.items():
            # Usamos el método calcula_distancia del registro de test
            distancia = registro_test.calcula_distancia(centroide, self.distancia)
            if distancia < menor_distancia:
                menor_distancia = distancia
                mejor_etiqueta = etiqueta

        return mejor_etiqueta
    


class Regresor_lineal_multiple(Modelo):
    """
    Aproximación heurística de una recta de regresión múltiple.
    """
    def __init__(self):
        super().__init__()
        self.coeficientes = []
        self.interseccion = 0.0 # También conocido como sesgo o "bias" (w0)

    def entrenar(self, dataset):
        super().entrenar(dataset)
        registros = dataset.registros
        
        if not registros:
            return

        num_atributos = len(registros[0].atributos)
        n = len(registros)

        # 1. Valores reales (y) y su media
        y = [reg.objetivo for reg in registros]
        media_y = sum(y) / n

        self.coeficientes = []
        medias_x = []

        # 2. Calcular los pesos (w_i) independientemente usando la varianza/covarianza
        for i in range(num_atributos):
            x_i = [reg.atributos[i] for reg in registros]
            media_x = sum(x_i) / n
            medias_x.append(media_x)

            # Covarianza (numerador) y varianza (denominador)
            numerador = sum((x_i[j] - media_x) * (y[j] - media_y) for j in range(n))
            denominador = sum((x_i[j] - media_x) ** 2 for j in range(n))

            if denominador == 0:
                peso = 0.0
            else:
                peso = numerador / denominador
            
            self.coeficientes.append(peso)

        # 3. Calcular la intersección o "corte con el eje" (w0)
        # w0 = media_y - (w1*x1 + w2*x2 + ... + wn*xn)
        suma_pesos_medias = sum(w * m for w, m in zip(self.coeficientes, medias_x))
        self.interseccion = media_y - suma_pesos_medias

    def predecir(self, registro_test):
        if not self.coeficientes:
            raise ValueError("El modelo no está entrenado.")
            
        # 1. Empezamos con el valor de la intersección (sesgo inicial)
        prediccion = self.interseccion
        
        # 2. Le sumamos el efecto de cada atributo multiplicado por su peso
        for w, x in zip(self.coeficientes, registro_test.atributos):
            prediccion += w * x
            
        return prediccion