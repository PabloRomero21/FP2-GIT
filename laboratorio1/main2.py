import os
from factorias import FactoriaCSV, FactoriaXLS
from modelos import Clasificador_kNN, Regresor_kNN
from dataset import DataSetClasificacion # Lo importamos para hacer el IF

def evaluar_modelo(dataset, k, distancia, pesos=None):
    """
    Evalúa el dataset dinámicamente:
    - Si es Clasificación: Devuelve % de Precisión (Mayor es mejor)
    - Si es Regresión: Devuelve Error Absoluto Medio - MAE (Menor es mejor)
    """
    # EL IF QUE PEDISTE: Comprobamos de qué tipo es el contenedor de datos
    if isinstance(dataset, DataSetClasificacion):
        modelo = Clasificador_kNN(k=k, distancia=distancia, pesos=pesos)
        modelo.entrenar(dataset)
        
        aciertos = 0
        for registro in dataset.registros:
            if modelo.predecir(registro) == registro.objetivo:
                aciertos += 1
        return (aciertos / len(dataset.registros)) * 100  # Devuelve Precisión
        
    else: # Si no es clasificación, es Regresión
        modelo = Regresor_kNN(k=k, distancia=distancia, pesos=pesos)
        modelo.entrenar(dataset)
        
        suma_errores = 0.0
        for registro in dataset.registros:
            error = abs(modelo.predecir(registro) - registro.objetivo)
            suma_errores += error
        return suma_errores / len(dataset.registros)  # Devuelve MAE


def ejecutar_bateria_pruebas(nombre_archivo, indice_obj, pesos_prueba, es_excel=False, es_regresion=False):
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(directorio_actual, nombre_archivo)
    
    print(f"\n{'='*60}")
    tipo_problema = "REGRESIÓN" if es_regresion else "CLASIFICACIÓN"
    print(f"🚀 INICIANDO BATERÍA DE PRUEBAS: {nombre_archivo} ({tipo_problema})")
    print(f"{'='*60}")
    
    # 1. Cargar el dataset con la factoría correcta
    if es_excel:
        dataset = FactoriaXLS.crear_dataset_clasificacion(ruta, indice_objetivo=indice_obj)
    elif es_regresion:
        dataset = FactoriaCSV.crear_dataset_regresion(ruta, indice_objetivo=indice_obj)
    else:
        dataset = FactoriaCSV.crear_dataset_clasificacion(ruta, indice_objetivo=indice_obj)
        
    # 2. Definir las combinaciones a probar
    ks_a_probar = [3, 5, 7, 9, 11, 13]
    distancias_a_probar = ["euclídea", "manhattan"]
    
    # Lógica para saber cuál es el "mejor":
    # En clasificación empezamos en 0 y subimos. En regresión empezamos en infinito y bajamos.
    mejor_metrica = float('inf') if es_regresion else 0.0
    mejor_config = ""
    unidad = "MAE (Error)" if es_regresion else "% Precisión"

    # 3. Bucle para probar Euclídea y Manhattan
    for k in ks_a_probar:
        for dist in distancias_a_probar:
            resultado = evaluar_modelo(dataset, k, dist)
            print(f"Probando k={k:2d} | Distancia: {dist.ljust(10)} -> {resultado:.2f} {unidad}")
            
            # Comprobamos si es el nuevo ganador
            if es_regresion and resultado < mejor_metrica:
                mejor_metrica = resultado
                mejor_config = f"k={k}, Distancia={dist}"
            elif not es_regresion and resultado > mejor_metrica:
                mejor_metrica = resultado
                mejor_config = f"k={k}, Distancia={dist}"

    # 4. Probar la distancia ponderada
    print("\n--- Probando Distancia Ponderada ---")
    for k in ks_a_probar:
        resultado = evaluar_modelo(dataset, k, "ponderada", pesos_prueba)
        print(f"Probando k={k:2d} | Distancia: ponderada -> {resultado:.2f} {unidad}")
        
        if es_regresion and resultado < mejor_metrica:
            mejor_metrica = resultado
            mejor_config = f"k={k}, Distancia=ponderada"
        elif not es_regresion and resultado > mejor_metrica:
            mejor_metrica = resultado
            mejor_config = f"k={k}, Distancia=ponderada"

    print(f"\n🏆 GANADOR PARA {nombre_archivo}: {mejor_config} con {mejor_metrica:.2f} {unidad}.")

def main():
    # 1. Prueba Iris (Clasificación)
    ejecutar_bateria_pruebas("iris.xlsx", indice_obj=-1, pesos_prueba=[0.5, 0.5, 1.5, 1.5], es_excel=True)

    # 2. Prueba Wine (Clasificación) - Objetivo al principio (0)
    pesos_wine = [1.0] * 12 + [2.0]
    ejecutar_bateria_pruebas("wine.csv", indice_obj=0, pesos_prueba=pesos_wine)

    # 3. Prueba Diabetes (Clasificación)
    pesos_diabetes = [1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0]
    ejecutar_bateria_pruebas("diabetes.csv", indice_obj=-1, pesos_prueba=pesos_diabetes)

    # 4. Prueba BostonHousing (Regresión) - Objetivo al final (-1)
    # Tenemos 13 atributos en BostonHousing. Vamos a darle más peso (2.0) al RM (nº de habitaciones, índice 5)
    pesos_boston = [1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    ejecutar_bateria_pruebas("BostonHousing.csv", indice_obj=-1, pesos_prueba=pesos_boston, es_regresion=True)

if __name__ == "__main__":
    main()