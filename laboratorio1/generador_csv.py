import csv
import random

def generar_dataset_csv(ruta_completa, num_registros=10, dimension=4):
    # Abrimos directamente el archivo en la ruta especificada
    # Si la carpeta 'laboratorio1' ya existe, simplemente creará el archivo dentro
    with open(ruta_completa, mode='w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        for _ in range(num_registros):
            fila = [random.uniform(0, 100) for _ in range(dimension)]
            escritor.writerow(fila)
    
    print(f"Archivo guardado en la carpeta existente: {ruta_completa}")


    