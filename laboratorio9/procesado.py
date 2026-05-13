from abc import ABC, abstractmethod
from registro import RegistroClasificacion, RegistroRegresion
from dataset import DataSetClasificacion, DataSetRegresion

class Preprocesamiento(ABC):
    @abstractmethod
    def ajustar(self, dataset): pass
    @abstractmethod
    def transformar_dataSet(self, dataset): pass
    @abstractmethod
    def transformar_registro(self, registro): pass

class NormalizadorMaxMin(Preprocesamiento):
    def __init__(self):
        self.minimos = []
        self.maximos = []

    def ajustar(self, dataset):
        # Calcula min/max de atributos y objetivo
        self.minimos, self.maximos = dataset.calcular_min_max()

    def transformar_dataSet(self, dataset):
        nuevo_ds = type(dataset)()
        nuevo_ds.nombres_atributos = dataset.nombres_atributos.copy()
        for reg in dataset.registros:
            nuevo_ds.agregar_registro(self.transformar_registro(reg))
        return nuevo_ds

    def transformar_registro(self, registro):
        n = len(registro.atributos)
        # Normalizamos atributos usando solo los índices correspondientes
        attrs_norm = registro.normalizar(self.minimos[:n], self.maximos[:n])
        
        obj_final = registro.objetivo
        # Si el registro tiene objetivo y conocemos el min/max del objetivo
        if hasattr(registro, 'objetivo') and len(self.minimos) > n:
            mi_obj, ma_obj = self.minimos[-1], self.maximos[-1]
            if ma_obj != mi_obj:
                obj_final = (registro.objetivo - mi_obj) / (ma_obj - mi_obj)
            else:
                obj_final = 0.0
            
        return type(registro)(attrs_norm, obj_final)

    def deshacer_transformacion_objetivo(self, valor_normalizado):
        """Convierte la predicción de [0,1] a la escala original."""
        if not self.minimos: return valor_normalizado
        min_obj, max_obj = self.minimos[-1], self.maximos[-1]
        return valor_normalizado * (max_obj - min_obj) + min_obj

class EstandarizadorZScore(Preprocesamiento):
    def __init__(self):
        self.medias = []
        self.desviaciones = []

    def ajustar(self, dataset):
        self.medias, self.desviaciones = dataset.calcular_medias_desviaciones()

    def transformar_dataSet(self, dataset):
        nuevo_ds = type(dataset)()
        nuevo_ds.nombres_atributos = dataset.nombres_atributos.copy()
        for reg in dataset.registros:
            nuevo_ds.agregar_registro(self.transformar_registro(reg))
        return nuevo_ds

    def transformar_registro(self, registro):
        n = len(registro.atributos)
        # IMPORTANTE: Usar los primeros n elementos
        attrs_std = registro.estandarizar(self.medias[:n], self.desviaciones[:n])
        
        obj_final = registro.objetivo
        if hasattr(registro, 'objetivo') and len(self.medias) > n:
            m_obj, d_obj = self.medias[-1], self.desviaciones[-1]
            obj_final = (registro.objetivo - m_obj) / d_obj if d_obj > 0.0000001 else 0.0
            
        return type(registro)(attrs_std, obj_final)

    def deshacer_transformacion_objetivo(self, valor_estandarizado):
        if not self.medias: return valor_estandarizado
        media_obj, desv_obj = self.medias[-1], self.desviaciones[-1]
        return (valor_estandarizado * desv_obj) + media_obj
    

