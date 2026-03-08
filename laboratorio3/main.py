import os
from factorias import*
from modelos import*
from math import sqrt

def main():

    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(directorio_actual, "BostonHousing.csv")
    
    print(f"Cargando dataset desde: {ruta_csv}...")
    nombre_dataset = os.path.basename(ruta_csv)
    
    dataset = FactoriaCSV.crear_dataset_regresion(ruta_csv)
    
    print(f"Datos cargados del dataset {nombre_dataset}")
    print(f"Total de registros: {len(dataset.registros)}\n")

    k_vecinos = int(sqrt(len(dataset.registros)))
    
    if k_vecinos % 2 == 0: 
        k_vecinos += 1
        
    tipo_distancia = "euclídea"

    
    modelo_knn = Regresor_kNN(k=k_vecinos, distancia=tipo_distancia)

    print(f"Entrenando modelo kNN con k={k_vecinos} y distancia '{tipo_distancia}'...")
    modelo_knn.entrenar(dataset)

# --- SECCIÓN DE EVALUACIÓN UNIFICADA ---
    total = len(dataset.registros)
    
    print("-" * 40)
    print("RESULTADOS DE LA EVALUACIÓN:")

    if isinstance(modelo_knn, Clasificador_kNN):
        aciertos = 0
        for registro in dataset.registros:
            if modelo_knn.predecir(registro) == registro.objetivo:
                aciertos += 1
        
        # Solo imprimimos métricas de CLASIFICACIÓN
        print(f"Modelo: CLASIFICACIÓN (kNN)")
        print(f"Total evaluados: {total}")
        print(f"Aciertos: {aciertos}")
        print(f"Fallos: {total - aciertos}")
        print(f"Precisión (Accuracy): {(aciertos/total)*100:.2f}%")

    elif isinstance(modelo_knn, Regresor_kNN):
        suma_error_abs = 0
        for registro in dataset.registros:
            error = abs(registro.objetivo - modelo_knn.predecir(registro))
            suma_error_abs += error
            
        mae = suma_error_abs / total
        # Solo imprimimos métricas de REGRESIÓN
        print(f"Modelo: REGRESIÓN (kNN)")
        print(f"Total evaluados: {total}")
        print(f"Error Medio Absoluto (MAE): {mae:.2f}")
        print(f"Interpretación: La IA se equivoca en promedio {mae:.2f} unidades.")

    print("-" * 40)

if __name__ == "__main__":
    main()