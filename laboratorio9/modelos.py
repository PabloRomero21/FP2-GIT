from abc import ABC, abstractmethod
from collections import Counter
import math
import random

class Modelo(ABC):
    def __init__(self):
        """
        Constructor de la clase abstracta Modelo.
        Inicializa el atributo datos_entrenamiento a nulo.
        """
        self.datos_entrenamiento = None

    def entrenar(self, dataset):
        """
        Recibe un objeto DataSet y lo guarda en el atributo de entrenamiento.
        """
        self.datos_entrenamiento = dataset

    @abstractmethod
    def predecir(self, registro):
        """
        Método abstracto que deben implementar las clases hijas.
        """
        pass


class Clasificador_kNN(Modelo):
    def __init__(self, k, distancia="euclídea", pesos=None):
        super().__init__()
        self.k = k
        self.distancia = distancia
        self.pesos = pesos

    def predecir(self, registro_test):
        if not self.datos_entrenamiento or not self.datos_entrenamiento.registros:
            return None
        
        # Obtenemos los k vecinos usando la lógica de la clase Registro
        indices_vecinos = registro_test.k_vecinos(
            self.datos_entrenamiento.registros, 
            self.k, 
            self.distancia, 
            self.pesos
        )
        
        clases_vecinos = [self.datos_entrenamiento.registros[idx].objetivo for idx in indices_vecinos]
        
        # La predicción es la clase más frecuente
        conteo = Counter(clases_vecinos)
        return conteo.most_common(1)[0][0]


class Regresor_kNN(Modelo):
    def __init__(self, k, pesos_atributos=None):
        """
        Constructor del regresor kNN para series temporales.
        """
        super().__init__()
        self.k = k
        self.pesos_atributos = pesos_atributos

    def predecir(self, registro_test):
        if not self.datos_entrenamiento or not self.datos_entrenamiento.registros:
            return 0.0
        
        # Calculamos distancias a todos los ejemplos de entrenamiento
        distancias = []
        for reg_train in self.datos_entrenamiento.registros:
            if self.pesos_atributos:
                # Usamos la distancia ponderada con los pesos optimizados
                d = registro_test.distancia_ponderada(reg_train, self.pesos_atributos)
            else:
                d = registro_test.distancia_euclidea(reg_train)
            distancias.append((d, reg_train.objetivo))
        
        # Ordenamos por cercanía
        distancias.sort(key=lambda x: x[0])
        vecinos = distancias[:self.k]
        
        # La predicción es la media aritmética de los objetivos de los vecinos
        return sum(v[1] for v in vecinos) / self.k

# En modelos.py -> Clase Regresor_kNN

    # En modelos.py -> Clase Regresor_kNN

    def optimizar_pesos_heuristica(self, dataset, iteraciones=50):
        # GUARDAMOS UNA SUBMUESTRA PARA ENTRENAMIENTO RÁPIDO
        # En lugar de buscar contra 10,000 registros, buscamos contra 500.
        todos = dataset.registros
        self.datos_entrenamiento_backup = dataset
        
        # Creamos un dataset temporal pequeño solo para la fase de optimización
        dataset_rapido = type(dataset)()
        dataset_rapido.registros = random.sample(todos, min(len(todos), 500))
        self.datos_entrenamiento = dataset_rapido
        
        num_atribs = len(todos[0].atributos)
        mejor_pesos = [random.random() for _ in range(num_atribs)]
        self.pesos_atributos = mejor_pesos
        
        mejor_mae = self._evaluar_mae_interno()
        print(f"Optimizando pesos (K={self.k})... MAE Inicial: {mejor_mae:.4f}")

        for i in range(iteraciones):
            # Feedback visual para que veas que se mueve
            print(f"  > Optimizando K={self.k}: {int((i/iteraciones)*100)}% completo", end="\r")
            
            candidato = mejor_pesos.copy()
            idx = random.randint(0, num_atribs - 1)
            candidato[idx] = max(0.0, min(1.0, candidato[idx] + random.uniform(-0.1, 0.1)))
            
            self.pesos_atributos = candidato
            mae_candidato = self._evaluar_mae_interno()
            
            if mae_candidato < mejor_mae:
                mejor_mae = mae_candidato
                mejor_pesos = candidato
            else:
                self.pesos_atributos = mejor_pesos
                
        # RESTAURAMOS el dataset completo para la predicción final de la tabla
        self.datos_entrenamiento = self.datos_entrenamiento_backup
        print(f"\n  K={self.k} optimizado.")

    def _evaluar_mae_interno(self):
        # Evaluamos sobre 20 registros aleatorios
        muestra = random.sample(self.datos_entrenamiento_backup.registros, 20)
        error_acumulado = 0.0
        for reg in muestra:
            pred = self.predecir(reg)
            error_acumulado += abs(reg.objetivo - pred)
        return error_acumulado / len(muestra)


class RectaRegresion(Modelo):
    def __init__(self, tasa=0.001, epocas=100):
        super().__init__()
        self.tasa = tasa
        self.epocas = epocas
        self.w = []      # Pesos (coeficientes)
        self.w0 = 0.0    # Intersección (bias)

    def entrenar(self, dataset):
        """
        Entrena el modelo usando los últimos 1000 registros para optimizar.
        """
        super().entrenar(dataset)
        
        todos = dataset.registros
        registros = todos[-1000:] if len(todos) > 1000 else todos
        
        if not registros:
            return

        num_atributos = len(registros[0].atributos)
        self.w = [0.0] * num_atributos
        self.w0 = 0.0
        
        for _ in range(self.epocas):
            for reg in registros:
                prediccion = self.w0 + sum(wi * xi for wi, xi in zip(self.w, reg.atributos))
                error = prediccion - reg.objetivo
                
                # Descenso de gradiente estocástico
                self.w0 -= self.tasa * error
                for i in range(num_atributos):
                    self.w[i] -= self.tasa * error * reg.atributos[i]

    def predecir(self, registro_test):
        if not self.w:
            return 0.0
        return self.w0 + sum(wi * xi for wi, xi in zip(self.w, registro_test.atributos))