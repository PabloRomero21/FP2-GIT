import os
from factorias import*
from modelos import*  # Asegúrate de importar tu regresor
from math import sqrt

def main():

    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(directorio_actual, "iris.xlsx")
    
    print(f"Cargando dataset desde: {ruta_csv}...")
    nombre_dataset = os.path.basename(ruta_csv)
    
    dataset = FactoriaXLS.crear_dataset_clasificacion(ruta_csv)
    
    print(f"Datos cargados del dataset {nombre_dataset}")
    print(f"Total de registros: {len(dataset.registros)}\n")

    k_vecinos = int(sqrt(len(dataset.registros)))
    
    if k_vecinos % 2 == 0: 
        k_vecinos += 1
        
    tipo_distancia = "euclídea"

    
    modelo_knn = Clasificador_kNN(k=k_vecinos, distancia=tipo_distancia)

    print(f"Entrenando modelo kNN con k={k_vecinos} y distancia '{tipo_distancia}'...")
    modelo_knn.entrenar(dataset)

    # CORRECCIÓN 2: Lógica de evaluación para Regresión
    total = len(dataset.registros)
    aciertos = 0
    fallos = 0
    for registro in dataset.registros:
        valor_predicho = modelo_knn.predecir(registro)
        valor_real = registro.objetivo
        if valor_predicho == valor_real:
            aciertos += 1
        else: fallos += 1


    
    print("-" * 40)
    print("RESULTADOS DE LA EVALUACIÓN:")
    print(f"Total evaluados: {total}")
    print(f"Aciertos:{aciertos}")
    print(f"Fallos:{fallos}")
    print(f"La IA acierta el {(aciertos/total)*100}% de las veces")
    print("-" * 40)

if __name__ == "__main__":
    main()