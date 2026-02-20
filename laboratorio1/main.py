import os
from generador_csv import generar_dataset_csv
from factoria import RegistroFactory
from registro import Registro

def main():
    # --- CONFIGURACIÓN DE RUTA DINÁMICA ---
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    nombre_archivo = "datos.csv"
    ruta_completa = os.path.join(directorio_actual, nombre_archivo)
    
    print("==========================================")
    print("   TEST INTEGRAL DE LA CLASE REGISTRO")
    print("==========================================\n")

    # 1. DETECCIÓN Y GENERACIÓN
    # Comprobamos si el archivo NO existe antes de generarlo
    if not os.path.exists(ruta_completa):
        print(f"[SISTEMA] El archivo {nombre_archivo} no existe. Generando uno nuevo...")
        generar_dataset_csv(ruta_completa, num_registros=10, dimension=4)
    else:
        print(f"[SISTEMA] Se ha detectado un archivo '{nombre_archivo}' previo. Usando datos existentes.")

    # 2. CARGA MEDIANTE FACTORÍA
    lista_de_registros = RegistroFactory.crear_desde_csv(ruta_completa)
    
    if not lista_de_registros:
        print("[ERROR] La lista de registros está vacía.")
        return

    # 3. PRUEBA DE LAS TRES DISTANCIAS
    print("\n[PASO 1] Probando tipos de distancias (Objetivo vs Registro ID 0):")
    objetivo = Registro([50.0, 50.0, 50.0, 50.0])
    otro = lista_de_registros[0]
    
    # Euclídea
    print(f"   - Euclídea:   {objetivo.calcula_distancia(otro, 'euclídea'):.4f}")
    # Manhattan
    print(f"   - Manhattan:  {objetivo.calcula_distancia(otro, 'manhattan'):.4f}")
    # Ponderada
    pesos = [0.5, 0.1, 0.2, 0.2]
    print(f"   - Ponderada:  {objetivo.calcula_distancia(otro, 'ponderada', pesos):.4f}")

    # 4. PRUEBA DE NORMALIZACIÓN
    print("\n[PASO 2] Probando Normalización:")
    minimos, maximos = [0.0]*4, [100.0]*4
    reg_norm = otro.normalizar(minimos, maximos)
    print(f"   - Original:    {otro}")
    print(f"   - Normalizado: {reg_norm}")

    # 5. PRUEBA DE K-VECINOS
    k = 3
    print(f"\n[PASO 3] Buscando los {k} vecinos más cercanos:")
    indices = objetivo.k_vecinos(lista_de_registros, k)
    print(f"   - Índices encontrados: {indices}")
    
    for idx in indices:
        d = objetivo.distancia_euclidea(lista_de_registros[idx])
        print(f"     * Registro {idx}: {lista_de_registros[idx]} | Distancia: {d:.4f}")

    print("\n==========================================")
    print("         TEST COMPLETADO CON ÉXITO")
    print("==========================================")

if __name__ == "__main__":
    main()