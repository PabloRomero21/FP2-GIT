import random
from abc import ABC, abstractmethod


"""

1. Nuevas Métricas de Regresión

Además del MAE (Error Absoluto Medio), añadiremos:

    MSE (Mean Squared Error - Error Cuadrático Medio): Penaliza mucho más los errores grandes al elevarlos al cuadrado. MSE=n1​∑(yi​−y^​i​)2

    RMSE (Root Mean Squared Error): Es la raíz cuadrada del MSE. Se usa mucho porque devuelve el error a la misma unidad de medida original (ej. euros, metros). RMSE=MSE​

    R² (Coeficiente de Determinación): Mide cuánta de la varianza de los datos es explicada por el modelo. Su valor ideal es 1.0. Si es 0 o negativo, tu modelo es peor que simplemente predecir la media de los datos siempre.

2. Nuevas Métricas de Clasificación

Además del Accuracy (Porcentaje de aciertos), añadiremos un enfoque Macro (calcula la métrica por cada clase y hace la media), que es ideal para datasets como Iris o Wine:

    Tasa de Error: El porcentaje de fallos (100−Accuracy).

    Precisión (Precision): De todas las veces que el modelo dijo "Es clase X", ¿cuántas acertó?

    Sensibilidad (Recall): De todas las que realmente eran "Clase X", ¿cuántas logró encontrar el modelo?

    F1-Score: Es la media armónica entre Precision y Recall. Muy útil para tener una métrica única y robusta.

"""




class Validacion(ABC):
    """
    Clase abstracta que actúa como evaluador de modelos de Machine Learning.
    Orquesta la división de datos, el preprocesamiento, el entrenamiento y la evaluación.
    """

    @abstractmethod
    def calcular_metricas(self, predichos, reales):
        """Método abstracto que las clases hijas implementarán (Accuracy o MAE)"""
        pass

    def validacion_simple(self, modelo, dataset, porcentaje, normalizador=None):
        """
        Validación Hold-Out adaptada a tu crear_subconjunto.
        """
        # 1. Copiamos y barajamos directamente los REGISTROS
        registros = dataset.registros.copy()
        import random
        random.shuffle(registros)
        
        # 2. Calculamos el punto de corte
        corte = int(len(registros) * porcentaje)
        registros_train = registros[:corte]
        registros_test = registros[corte:]
        
        # 3. Usamos TU método pasándole las listas de registros
        ds_train = dataset.crear_subconjunto(registros_train)
        ds_test = dataset.crear_subconjunto(registros_test)
        
        # 4. PREPROCESAMIENTO (Si hay normalizador)
        if normalizador is not None:
            normalizador.ajustar(ds_train)
            ds_train = normalizador.transformar_dataSet(ds_train)
            ds_test = normalizador.transformar_dataSet(ds_test)
            
        # 5. Entrenamos y predecimos
        modelo.entrenar(ds_train)
        
        predichos = []
        reales = []
        for registro in ds_test.registros:
            predichos.append(modelo.predecir(registro))
            reales.append(registro.objetivo)
            
        # 6. Calcular y devolver la métrica
        return self.calcular_metricas(predichos, reales)


    def validacion_cruzada(self, modelo, dataset, m, normalizador=None):
        """
        Validación Cross-Validation adaptada a tu crear_subconjunto 
        y a las nuevas métricas (diccionarios).
        """
        import random
        registros = dataset.registros.copy()
        random.shuffle(registros)
        
        tamano_bolsa = len(registros) // m
        resultados_iteraciones = []
        
        for i in range(m):
            inicio = i * tamano_bolsa
            fin = (i + 1) * tamano_bolsa if i != m - 1 else len(registros)
            
            # Separamos las listas de registros directamente
            registros_test = registros[inicio:fin]
            registros_train = registros[:inicio] + registros[fin:]
            
            # Usamos TU método
            ds_train = dataset.crear_subconjunto(registros_train)
            ds_test = dataset.crear_subconjunto(registros_test)
            
            # Preprocesamiento
            if normalizador is not None:
                normalizador.ajustar(ds_train)
                ds_train = normalizador.transformar_dataSet(ds_train)
                ds_test = normalizador.transformar_dataSet(ds_test)
                
            # Entrenamiento y evaluación
            modelo.entrenar(ds_train)
            
            predichos = []
            reales = []
            for reg in ds_test.registros:
                predichos.append(modelo.predecir(reg))
                reales.append(reg.objetivo)
                
            # Aquí recibimos un DICCIONARIO de métricas
            resultado_bolsa = self.calcular_metricas(predichos, reales)
            resultados_iteraciones.append(resultado_bolsa)
            
        # --- LA NUEVA MAGIA PARA CALCULAR LA MEDIA DEL DICCIONARIO ---
        metricas_medias = {}
        # Extraemos las claves del primer diccionario (ej: "Accuracy (%)", "MAE", etc.)
        claves_metricas = resultados_iteraciones[0].keys()
        
        for clave in claves_metricas:
            # Sumamos el valor de esta métrica específica en todas las 'm' iteraciones
            suma_metrica = sum(iteracion[clave] for iteracion in resultados_iteraciones)
            # Lo dividimos entre 'm' para sacar su media
            metricas_medias[clave] = suma_metrica / m
            
        return metricas_medias


class ValidacionClasificacion(Validacion):
    """
    Calcula Accuracy, Tasa de Error, Precision, Recall y F1-Score (Macro).
    """
    def calcular_metricas(self, predichos, reales):
        if not reales: return {}
        
        n = len(reales)
        aciertos = 0
        clases = set(reales)
        
        # Diccionario para contar Verdaderos Positivos (TP), Falsos Positivos (FP) y Falsos Negativos (FN)
        dicc_clases = {c: {"TP": 0, "FP": 0, "FN": 0} for c in clases}
        
        for p, r in zip(predichos, reales):
            p_str, r_str = str(p), str(r)
            
            if p_str == r_str:
                aciertos += 1
                if p_str in dicc_clases: dicc_clases[p_str]["TP"] += 1
            else:
                if p_str in dicc_clases: dicc_clases[p_str]["FP"] += 1
                if r_str in dicc_clases: dicc_clases[r_str]["FN"] += 1
                
        # Métricas globales
        accuracy = (aciertos / n) * 100
        
        # Cálculo Macro (media de las métricas de todas las clases)
        suma_precision, suma_recall = 0.0, 0.0
        
        for c, counts in dicc_clases.items():
            tp, fp, fn = counts["TP"], counts["FP"], counts["FN"]
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            
            suma_precision += precision
            suma_recall += recall
            
        macro_precision = (suma_precision / len(clases)) * 100
        macro_recall = (suma_recall / len(clases)) * 100
        
        # Evitar división por cero en F1
        if (macro_precision + macro_recall) > 0:
            f1_score = 2 * (macro_precision * macro_recall) / (macro_precision + macro_recall)
        else:
            f1_score = 0.0
        
        return {
            "Accuracy (%)": accuracy,
            "Tasa Error (%)": 100 - accuracy,
            "Precision Macro (%)": macro_precision,
            "Recall Macro (%)": macro_recall,
            "F1-Score Macro (%)": f1_score
        }

class ValidacionRegresion(Validacion):
    """
    Calcula MAE, MSE, RMSE y R^2.
    """
    def calcular_metricas(self, predichos, reales):
        if not reales: return {}
        
        n = len(reales)
        suma_errores_abs = 0.0
        suma_errores_cuad = 0.0
        media_reales = sum(float(r) for r in reales) / n
        suma_varianza_total = 0.0
        
        for p, r in zip(predichos, reales):
            p_float, r_float = float(p), float(r)
            error = p_float - r_float
            
            suma_errores_abs += abs(error)
            suma_errores_cuad += error ** 2
            suma_varianza_total += (r_float - media_reales) ** 2
            
        mae = suma_errores_abs / n
        mse = suma_errores_cuad / n
        rmse = mse ** 0.5
        
        # R2 = 1 - (Suma de Errores Cuadrados / Suma Varianza Total)
        r2 = 1 - (suma_errores_cuad / suma_varianza_total) if suma_varianza_total != 0 else 0.0
        
        return {
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse,
            "R2": r2
        }
    

class SeleccionAtributos:
    """
    Clase utilitaria para seleccionar los mejores atributos de un dataset.
    Aunque esté en validacion.py, sus resultados se suelen usar para preprocesar.
    """
    @staticmethod
    def seleccion_correlacion(dataset, p):
        import math
        if not dataset.registros:
            return []
            
        # Extraemos los valores objetivo (Y) como números reales
        y = [float(r.objetivo) for r in dataset.registros]
        n = len(y)
        media_y = sum(y) / n
        
        num_atributos = len(dataset.registros[0].atributos)
        correlaciones = []
        
        # Calculamos Pearson para cada columna de atributos (X)
        for i in range(num_atributos):
            x = [r.atributos[i] for r in dataset.registros]
            media_x = sum(x) / n
            
            numerador = sum((x[j] - media_x) * (y[j] - media_y) for j in range(n))
            denominador_x = sum((x[j] - media_x) ** 2 for j in range(n))
            denominador_y = sum((y[j] - media_y) ** 2 for j in range(n))
            
            # Evitar divisiones por cero si una columna es constante
            if denominador_x == 0 or denominador_y == 0:
                r = 0.0
            else:
                r = numerador / math.sqrt(denominador_x * denominador_y)
                
            # Guardamos el valor absoluto (nos importa la fuerza de la relación, no el signo) 
            # y el índice de la columna
            correlaciones.append((abs(r), i))
            
        # Ordenamos de mayor a menor correlación
        correlaciones.sort(key=lambda item: item[0], reverse=True)
        
        # Calculamos cuántos atributos debemos devolver según el porcentaje 'p'
        num_mantener = max(1, int(num_atributos * (p / 100.0)))
        
        # Extraemos solo los índices originales de esos 'num_mantener' mejores atributos
        mejores_indices = [item[1] for item in correlaciones[:num_mantener]]
        
        return mejores_indices
    
    @staticmethod
    def calcular_pesos_pearson(dataset):
        """
        Calcula el coeficiente de correlación de Pearson de cada atributo con 
        el valor objetivo y devuelve sus valores absolutos como vector de pesos.
        Ideal para Regresión.
        """
        import math
        if not dataset.registros:
            return []
            
        # Asumimos que el objetivo se puede convertir a float (Regresión o Clasificación Binaria Numérica)
        try:
            y = [float(r.objetivo) for r in dataset.registros]
        except ValueError:
            raise TypeError("Para calcular Pearson, el objetivo debe ser numérico.")
            
        n = len(y)
        media_y = sum(y) / n
        num_atributos = len(dataset.registros[0].atributos)
        pesos = []
        
        for i in range(num_atributos):
            x = [r.atributos[i] for r in dataset.registros]
            media_x = sum(x) / n
            
            numerador = sum((x[j] - media_x) * (y[j] - media_y) for j in range(n))
            denominador_x = sum((x[j] - media_x) ** 2 for j in range(n))
            denominador_y = sum((y[j] - media_y) ** 2 for j in range(n))
            
            if denominador_x == 0 or denominador_y == 0:
                r = 0.0
            else:
                r = numerador / math.sqrt(denominador_x * denominador_y)
                
            # El peso es el valor absoluto de la correlación
            pesos.append(abs(r))
            
        return pesos
    
    @staticmethod
    def calcular_pesos_relief(dataset, iteraciones=100):
        """
        Implementa el algoritmo Relief original para ponderar atributos.
        Ideal para Clasificación.
        """
        import random
        if not dataset.registros:
            return []
            
        num_atributos = len(dataset.registros[0].atributos)
        pesos = [0.0] * num_atributos
        
        # Necesitamos los mínimos y máximos para normalizar las diferencias (evitar que 
        # un atributo grande como el 'precio' eclipse a uno pequeño).
        # ¡Usamos el método que ya tenías programado en DataSet!
        minimos, maximos = dataset.calcular_min_max()
        rangos = [maximos[i] - minimos[i] for i in range(num_atributos)]
        
        registros = dataset.registros
        n = len(registros)
        iteraciones = min(iteraciones, n) # Evitamos hacer más iteraciones que datos disponibles
        
        # Seleccionamos muestras al azar para agilizar el proceso
        muestras = random.sample(registros, iteraciones)
        
        for r_actual in muestras:
            distancia_hit = float('inf')
            distancia_miss = float('inf')
            hit = None
            miss = None
            
            # Buscamos el Hit (misma clase) y Miss (distinta clase) más cercanos
            for r_otro in registros:
                if r_actual is r_otro:
                    continue
                
                # Usamos tu distancia euclídea base
                dist = r_actual.distancia_euclidea(r_otro)
                
                if str(r_actual.objetivo) == str(r_otro.objetivo):
                    if dist < distancia_hit:
                        distancia_hit = dist
                        hit = r_otro
                else:
                    if dist < distancia_miss:
                        distancia_miss = dist
                        miss = r_otro
                        
            # Actualizamos los pesos
            if hit and miss:
                for i in range(num_atributos):
                    rango = rangos[i] if rangos[i] > 0 else 1.0 # Evitamos división por cero
                    
                    # Diferencia normalizada entre 0 y 1
                    diff_hit = abs(r_actual.atributos[i] - hit.atributos[i]) / rango
                    diff_miss = abs(r_actual.atributos[i] - miss.atributos[i]) / rango
                    
                    # Fórmula de Relief: W = W - (diff_hit/m) + (diff_miss/m)
                    pesos[i] = pesos[i] - (diff_hit / iteraciones) + (diff_miss / iteraciones)

        # Los atributos con pesos negativos se consideran inútiles (perjudican más de lo que ayudan).
        # Los forzamos a 0 para que la distancia ponderada los ignore por completo.
        pesos_finales = [max(0.0, w) for w in pesos]
        
        return pesos_finales