import os

# ==========================================
# FIJAR EL DIRECTORIO DE TRABAJO AL SCRIPT
# ==========================================
DIRECTORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIRECTORIO_SCRIPT)

# Importamos TODAS las clases de tu framework
from factorias import *
from modelos import Clasificador_kNN, Clasificador_centroide, Regresor_kNN, Regresor_lineal_multiple
from procesado import NormalizadorMaxMin, NormalizadorZ_Score, FiltroVarianza, FiltroENN
from validacion import ValidacionClasificacion, ValidacionRegresion, SeleccionAtributos

def verificar_entorno(archivos):
    print(f"--- VERIFICANDO DATASETS EN: {DIRECTORIO_SCRIPT} ---")
    archivos_actuales = os.listdir(DIRECTORIO_SCRIPT)
    faltantes = [a for a in archivos if a not in archivos_actuales]
    if faltantes:
        print("\n[ERROR] Faltan los siguientes archivos:")
        for f in faltantes: print(f"  -> {f}")
        return False
    print("  [OK] Todos los archivos encontrados.\n")
    return True

# ==========================================
# PRUEBA 1: DIABETES (Clasificación Binaria)
# ==========================================
def prueba_diabetes():
    print("="*60)
    print(" PRUEBA 1: DIABETES | kNN + Filtro Varianza + MaxMin + CV")
    print("="*60)
    # Objetivo al final (-1)
    dataset = FactoriaCSV.crear_dataset_clasificacion("diabetes.csv", indice_objetivo=-1)
    
    # 1. Preprocesado: Filtro de Varianza
    filtro_var = FiltroVarianza(umbral=0.01)
    filtro_var.ajustar(dataset)
    dataset_limpio = filtro_var.transformar_dataSet(dataset)
    
    # 2. Selección de Atributos: Relief
    print("-> Calculando Pesos Relief...")
    pesos = SeleccionAtributos.calcular_pesos_relief(dataset_limpio, iteraciones=50)
    print(f"   Mejores atributos (pesos): {[round(p, 3) for p in pesos[:3]]}...")

    # 3. Validación Cruzada con Normalizador MaxMin
    validador = ValidacionClasificacion()
    modelo = Clasificador_kNN(k=5, distancia="euclídea")
    normalizador = NormalizadorMaxMin()
    
    resultados = validador.validacion_cruzada(modelo, dataset_limpio, m=5, normalizador=normalizador)
    print("\n[Resultados CV - Diabetes]")
    for metrica, valor in resultados.items(): print(f"  * {metrica}: {valor:.4f}")

# ==========================================
# PRUEBA 2: IRIS (Clasificación Multiclase)
# ==========================================
def prueba_iris():
    print("\n" + "="*60)
    print(" PRUEBA 2: IRIS | Centroides + Filtro ENN + Z-Score + Hold-Out")
    print("="*60)
    # Archivo con nombre especial, objetivo al final (-1)
    dataset = FactoriaXLS.crear_dataset_clasificacion("iris.xlsx", indice_objetivo=-1)
    
    # 1. Preprocesado: Filtro ENN (Limpieza de ruido)
    print("-> Aplicando Filtro ENN...")
    filtro_enn = FiltroENN(k=3)
    dataset_limpio = filtro_enn.transformar_dataSet(dataset)
    print(f"   Registros originales: {len(dataset.registros)} | Tras ENN: {len(dataset_limpio.registros)}")

    # 2. Validación Simple (Hold-out) con Centroide y Normalizador Z-Score
    validador = ValidacionClasificacion()
    modelo = Clasificador_centroide()
    normalizador = NormalizadorZ_Score()
    
    resultados = validador.validacion_simple(modelo, dataset_limpio, porcentaje=0.7, normalizador=normalizador)
    print("\n[Resultados Hold-Out - Iris]")
    for metrica, valor in resultados.items(): print(f"  * {metrica}: {valor:.4f}")

# ==========================================
# PRUEBA 3: WINE (Clasificación Multiclase)
# ==========================================
def prueba_wine():
    print("\n" + "="*60)
    print(" PRUEBA 3: WINE | kNN (Manhattan) + Sin Filtro + MaxMin")
    print("="*60)
    # ¡OJO AQUÍ! En wine.csv la clase a predecir es la PRIMERA columna (índice 0)
    dataset = FactoriaCSV.crear_dataset_clasificacion("wine.csv", indice_objetivo=0)
    
    # Validación con distancia Manhattan
    validador = ValidacionClasificacion()
    modelo = Clasificador_kNN(k=3, distancia="manhattan")
    normalizador = NormalizadorMaxMin()
    
    resultados = validador.validacion_cruzada(modelo, dataset, m=3, normalizador=normalizador)
    print("\n[Resultados CV - Wine]")
    for metrica, valor in resultados.items(): print(f"  * {metrica}: {valor:.4f}")

# ==========================================
# PRUEBA 4: BOSTON HOUSING (Regresión)
# ==========================================
def prueba_boston():
    print("\n" + "="*60)
    print(" PRUEBA 4: BOSTON | Regresores + Pearson + Z-Score")
    print("="*60)
    # El valor continuo (MEDV) está en la penúltima columna (-2)
    dataset = FactoriaCSV.crear_dataset_regresion("BostonHousing.csv", indice_objetivo=-2)
    
    # 1. Selección de Atributos: Pearson
    print("-> Calculando Pesos Pearson...")
    pesos = SeleccionAtributos.calcular_pesos_pearson(dataset)
    for nombre, peso in list(zip(dataset.nombres_atributos, pesos))[:3]:
        print(f"   Peso '{nombre}': {peso:.4f}")

    validador = ValidacionRegresion()
    normalizador = NormalizadorZ_Score()
    
    # Prueba A: Regresor Lineal Múltiple
    print("\n-> Evaluando Regresor Lineal Múltiple (Hold-Out)...")
    mod_lineal = Regresor_lineal_multiple()
    res_lineal = validador.validacion_simple(mod_lineal, dataset, porcentaje=0.7, normalizador=normalizador)
    for m, v in res_lineal.items(): print(f"  * {m}: {v:.4f}")
        
    # Prueba B: Regresor kNN
    print("\n-> Evaluando Regresor kNN (k=5, CV)...")
    mod_knn = Regresor_kNN(k=5, distancia="euclídea")
    res_knn = validador.validacion_cruzada(mod_knn, dataset, m=5, normalizador=normalizador)
    for m, v in res_knn.items(): print(f"  * {m}: {v:.4f}")

# ==========================================
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    DATASETS = [
        "diabetes.csv", 
        "iris.xlsx", 
        "wine.csv", 
        "BostonHousing.csv"
    ]
    
    if verificar_entorno(DATASETS):
        prueba_diabetes()
        prueba_iris()
        prueba_wine()
        prueba_boston()
        print("\n" + "*"*60)
        print("  ¡TODAS LAS PRUEBAS FINALIZADAS CON ÉXITO!  ")
        print("*"*60)