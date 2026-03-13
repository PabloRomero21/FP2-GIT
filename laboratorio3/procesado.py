from abc import ABC, abstractmethod
from registro import RegistroClasificacion, RegistroRegresion
from dataset import DataSetClasificacion, DataSetRegresion

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




class NormalizadorMaxMin(Preprocesamiento):
    def __init__(self):
        """
        Constructor que inicializa las listas de máximos y mínimos a vacío.
        """
        self.minimos = []
        self.maximos = []

    def ajustar(self, dataset):
        """
        Calcula y guarda los mínimos y máximos a partir del dataset de entrenamiento.
        """
        # Usamos la función que ya tenías programada en dataset.py
        self.minimos, self.maximos = dataset.calcular_min_max()

    def transformar_registro(self, registro):
        """
        Aplica la fórmula matemática (x - min) / (max - min) a los atributos 
        de un registro y devuelve un NUEVO registro normalizado.
        """
        if not self.minimos or not self.maximos:
            raise ValueError("Error: Debes llamar a ajustar() antes de transformar.")

        atributos_normalizados = []
        
        # Recorremos cada valor junto con su mínimo y máximo correspondiente
        for valor, min_val, max_val in zip(registro.atributos, self.minimos, self.maximos):
            # Prevención de división por cero (por si toda una columna tiene el mismo número)
            if max_val == min_val:
                atributos_normalizados.append(0.0)
            else:
                # Fórmula de normalización Max-Min
                nuevo_valor = (valor - min_val) / (max_val - min_val)
                atributos_normalizados.append(nuevo_valor)

        # Devolvemos un objeto nuevo del MISMO TIPO que el original
        if isinstance(registro, RegistroClasificacion):
            return RegistroClasificacion(atributos_normalizados, registro.objetivo)
        elif isinstance(registro, RegistroRegresion):
            return RegistroRegresion(atributos_normalizados, registro.objetivo)
        else:
            raise TypeError("Tipo de registro desconocido.")

    def transformar_dataSet(self, dataset):
        """
        Devuelve un NUEVO DataSet con todos sus registros normalizados.
        """
        # 1. Creamos un nuevo contenedor del mismo tipo que el original
        if isinstance(dataset, DataSetClasificacion):
            nuevo_dataset = DataSetClasificacion()
        elif isinstance(dataset, DataSetRegresion):
            nuevo_dataset = DataSetRegresion()
        else:
            raise TypeError("Tipo de DataSet desconocido.")

        # 2. Copiamos los nombres de los atributos (cabeceras)
        nuevo_dataset.nombres_atributos = dataset.nombres_atributos.copy()

        # 3. Normalizamos registro a registro usando nuestra propia función
        for registro in dataset.registros:
            registro_norm = self.transformar_registro(registro)
            nuevo_dataset.agregar_registro(registro_norm)

        return nuevo_dataset
    


class NormalizadorZ_Score(Preprocesamiento):
    def __init__(self):
        """Inicializa las listas de medias y desviaciones a vacío."""
        self.medias = []
        self.desviaciones = []

    def ajustar(self, dataset):
        """
        Calcula las medias y desviaciones típicas mediante el 
        correspondiente método de DataSet.
        """
        self.medias, self.desviaciones = dataset.calcular_medias_desviaciones()

    def transformar_registro(self, registro):
        """
        Recibe un Registro y devuelve otro estandarizado usando
        el método de la clase Registro.
        """
        if not self.medias or not self.desviaciones:
            raise ValueError("Error: Debes llamar a ajustar() antes de transformar.")

        # Usamos el método que acabamos de crear en la clase Registro
        nuevos_atributos = registro.estandarizar(self.medias, self.desviaciones)

        # Devolvemos un objeto nuevo del mismo tipo
        if isinstance(registro, RegistroClasificacion):
            return RegistroClasificacion(nuevos_atributos, registro.objetivo)
        elif isinstance(registro, RegistroRegresion):
            return RegistroRegresion(nuevos_atributos, registro.objetivo)
        else:
            raise TypeError("Tipo de registro desconocido.")

    def transformar_dataSet(self, dataset):
        """
        Recibe un DataSet y devuelve otro con sus registros estandarizados.
        """
        # 1. Creamos un nuevo contenedor del mismo tipo
        if isinstance(dataset, DataSetClasificacion):
            nuevo_dataset = DataSetClasificacion()
        elif isinstance(dataset, DataSetRegresion):
            nuevo_dataset = DataSetRegresion()
        else:
            raise TypeError("Tipo de DataSet desconocido.")

        # 2. Copiamos los nombres de las cabeceras
        nuevo_dataset.nombres_atributos = dataset.nombres_atributos.copy()

        # 3. Transformamos y añadimos cada registro
        for registro in dataset.registros:
            registro_estandarizado = self.transformar_registro(registro)
            nuevo_dataset.agregar_registro(registro_estandarizado)

        return nuevo_dataset
    


class FiltroVarianza(Preprocesamiento):
    """
    Elimina los atributos cuya varianza sea menor o igual a un umbral dado.
    """
    def __init__(self, umbral=0.0):
        self.umbral = umbral
        self.indices_a_eliminar = []

    def ajustar(self, dataset):
        if not dataset.registros: return
        
        num_atributos = len(dataset.registros[0].atributos)
        n = len(dataset.registros)
        self.indices_a_eliminar = []
        
        for i in range(num_atributos):
            columna = [r.atributos[i] for r in dataset.registros]
            media = sum(columna) / n
            varianza = sum((x - media) ** 2 for x in columna) / n
            
            if varianza <= self.umbral:
                self.indices_a_eliminar.append(i)

    def transformar_dataSet(self, dataset):
        if not self.indices_a_eliminar:
            return dataset # No hay nada que filtrar
            
        # Usamos el método polimórfico que creaste en la Etapa anterior
        return dataset.eliminar_atributos(self.indices_a_eliminar)

    def transformar_registro(self, registro):
        if not self.indices_a_eliminar:
            return registro
            
        nuevos_atributos = [val for i, val in enumerate(registro.atributos) 
                            if i not in self.indices_a_eliminar]
                            
        # Devolvemos un clon del mismo tipo
        return type(registro)(nuevos_atributos, registro.objetivo)
    

class FiltroENN(Preprocesamiento):
    """
    Edited Nearest Neighbor (ENN). Elimina ejemplos que están rodeados
    por una mayoría de ejemplos de otra clase (ruido en la frontera).
    """
    def __init__(self, k=3):
        self.k = k

    def ajustar(self, dataset):
        # ENN no requiere calcular métricas globales previas como la media.
        pass

    def transformar_dataSet(self, dataset):
        from collections import Counter
        
        if not isinstance(dataset, DataSetClasificacion):
            raise TypeError("El filtro ENN solo se aplica a problemas de Clasificación.")
            
        # Instanciamos el nuevo contenedor limpio
        nuevo_dataset = DataSetClasificacion()
        nuevo_dataset.nombres_atributos = dataset.nombres_atributos.copy()
        
        for i, registro in enumerate(dataset.registros):
            # 1. Separar el registro actual del resto para no compararlo consigo mismo
            otros_registros = dataset.registros[:i] + dataset.registros[i+1:]
            
            # 2. Buscar sus k vecinos más cercanos (¡Usamos la inteligencia de Registro!)
            indices_vecinos = registro.k_vecinos(otros_registros, self.k)
            clases_vecinos = [otros_registros[idx].objetivo for idx in indices_vecinos]
            
            # 3. Determinar la clase mayoritaria de su vecindario
            clase_mayoritaria = Counter(clases_vecinos).most_common(1)[0][0]
            
            # 4. Si el registro pertenece a la misma clase que sus vecinos, se conserva
            if registro.objetivo == clase_mayoritaria:
                nuevo_dataset.agregar_registro(registro)
                
        return nuevo_dataset

    def transformar_registro(self, registro):
        # La limpieza de ejemplos se aplica sobre un conjunto entero, 
        # a un registro aislado de test simplemente lo dejamos pasar inalterado.
        return registro
    

