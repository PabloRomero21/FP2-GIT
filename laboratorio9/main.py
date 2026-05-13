import pandas as pd
import numpy as np
from factoria import FactoriaSerieTemporal
from modelos import Regresor_kNN, RectaRegresion
from registro import RegistroRegresion
from dataset import DataSetRegresion

def calcular_mae(reales, predicciones):
    return sum(abs(r - p) for r, p in zip(reales, predicciones)) / len(reales)

def obtener_datos():
    try:
        df_train = pd.read_excel("serie_temporal_alumnos.xlsx")
        valores_train = df_train.iloc[:, 1].tolist()
        df_test = pd.read_excel("serie_temporal_test.xlsx")
        valores_test = df_test.iloc[:, 1].tolist()
        return valores_train, valores_test
    except Exception as e:
        print(f"Error al cargar archivos: {e}")
        return None, None

def calcular_pesos_correlacion(ph, valores_train):
    serie = pd.Series(valores_train)
    df_lags = pd.DataFrame()
    for i in range(ph, 0, -1):
        df_lags[f'Lag_{i}'] = serie.shift(i)
    df_lags['Obj'] = serie
    df_lags = df_lags.dropna()
    corrs = [abs(df_lags[f'Lag_{i}'].corr(df_lags['Obj'])) for i in range(ph, 0, -1)]
    suma = sum(corrs)
    return [c / suma for c in corrs] if suma != 0 else [1.0/ph] * ph

def tabla_recta_regresion(valores_train, valores_test):
    experimentos = [(12, 1e-07), (24, 1e-07), (48, 1e-07), (12, 1e-08), (24, 1e-08), (48, 1e-08)]
    print("\n=========================================================================")
    print("RECTA DE REGRESIÓN (MAE)")
    print("=========================================================================")
    print(f"{'PH':<4} | {'Tasa':<10} | {'Min-Max?':<8} | {'Z-score?':<8} | {'MAE FH=24'}")
    print("-" * 75)
    for ph, tasa in experimentos:
        ds_train = DataSetRegresion()
        for i in range(len(valores_train) - ph):
            ds_train.agregar_registro(RegistroRegresion(valores_train[i:i+ph], valores_train[i+ph]))
        modelo = RectaRegresion(tasa=tasa, epocas=500)
        modelo.entrenar(ds_train)
        ventana = valores_train[-ph:]
        preds = []
        for _ in range(24):
            reg = RegistroRegresion(ventana, 0.0)
            p = modelo.predecir(reg)
            preds.append(p)
            ventana.pop(0)
            ventana.append(p)
        print(f"{ph:<4} | {tasa:<10} | {'No':<8} | {'No':<8} | {calcular_mae(valores_test[:24], preds):.4f}")

def tabla_knn_ponderado(valores_train, valores_test):
    phs, ks = [6, 12, 24, 48], [1, 3, 5]
    print("\n=========================================================================")
    print("kNN PONDERADO CON CORRELACIÓN")
    print("=========================================================================")
    print(f"{'PH':<4} | {'K':<4} | {'MAE FH=24 (29/12/2026)':<22}")
    print("-" * 45)
    for ph in phs:
        ds_train = DataSetRegresion()
        for i in range(len(valores_train) - ph):
            ds_train.agregar_registro(RegistroRegresion(valores_train[i:i+ph], valores_train[i+ph]))
        pesos = calcular_pesos_correlacion(ph, valores_train)
        for k in ks:
            modelo = Regresor_kNN(k=k)
            modelo.pesos_atributos = pesos
            modelo.entrenar(ds_train)
            ventana = valores_train[-ph:]
            preds = []
            for _ in range(24):
                p = modelo.predecir(RegistroRegresion(ventana, 0.0))
                preds.append(p); ventana.pop(0); ventana.append(p)
            print(f"{ph:<4} | {k:<4} | {calcular_mae(valores_test[:24], preds):.4f}")

def tabla_knn_heuristica(valores_train, valores_test, ph_mejor=24):
    ks = [1, 3, 5]
    print("\n=========================================================================")
    print(f"kNN CON HEURÍSTICA (PH={ph_mejor})")
    print("=========================================================================")
    print(f"{'K':<4} | {'MAE FH=24 (29/12/2026)':<22}")
    print("-" * 35)
    
    ds_train = DataSetRegresion()
    # Importante: Poblar nombres_atributos para que num_atribs no sea 0
    ds_train.nombres_atributos = [f"Lag{i}" for i in range(ph_mejor)]
    
    for i in range(len(valores_train) - ph_mejor):
        ds_train.agregar_registro(RegistroRegresion(valores_train[i:i+ph_mejor], valores_train[i+ph_mejor]))
    
# En main.py -> dentro de tabla_knn_heuristica

    for k in ks:
        modelo = Regresor_kNN(k=k)
        # Reducimos a 20 iteraciones para que la tabla se genere en un tiempo razonable
        modelo.optimizar_pesos_heuristica(ds_train, iteraciones=20)
        
        ventana = valores_train[-ph_mejor:]
        preds = []
        for _ in range(24):
            p = modelo.predecir(RegistroRegresion(ventana, 0.0))
            preds.append(p)
            ventana.pop(0)
            ventana.append(p)
        
        print(f"{k:<4} | {calcular_mae(valores_test[:24], preds):.4f}")

def main():
    v_train, v_test = obtener_datos()
    if v_train and v_test:
        tabla_recta_regresion(v_train, v_test)
        tabla_knn_ponderado(v_train, v_test)
        # Ejecutamos la heurística con el PH que mejor resultado dio antes
        tabla_knn_heuristica(v_train, v_test, ph_mejor=24)

if __name__ == "__main__":
    main()