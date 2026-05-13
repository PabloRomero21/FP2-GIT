import numpy as np
import retos_optimizacion as reto

# Importamos nuestros 5 algoritmos estrella
from algoritmos import (
    BusquedaAleatoria, 
    HillClimbing, 
    RecocidoSimulado, 
    BusquedaLocalIterada, 
    BusquedaVecindadVariable
)

if __name__ == "__main__":
    # 1. REQUISITO: Semilla para reproducibilidad de los experimentos
    np.random.seed(1)
    
    # 2. REQUISITO: Presupuesto estricto
    PRESUPUESTO_TOTAL = 10000
    PRESUPUESTO_GRID = 2000  # Dedicamos el 20% a buscar parámetros

    # Convertimos la lista de funciones a tuplas con nombres para las tablas
    funciones_a_evaluar = [
        ("funcion_1", reto.Funcion_1), 
        ("funcion_2", reto.Funcion_2), 
        ("funcion_3", reto.Funcion_3), 
        ("funcion_4", reto.Funcion_4)
    ]

    # Diccionario/Lista de algoritmos con su "Cuadrícula" (Grid)
    configuraciones_algoritmos = [
        ("Algoritmo 1", BusquedaAleatoria, []), 
        
        ("Algoritmo 2", HillClimbing, [
            {'tamano_paso': 0.1}, 
            {'tamano_paso': 0.5}, 
            {'tamano_paso': 1.5}, 
            {'tamano_paso': 3.0}
        ]),
        
        ("Algoritmo 3", RecocidoSimulado, [
            {'temperatura_inicial': 100.0, 'tasa_enfriamiento': 0.90},
            {'temperatura_inicial': 1000.0, 'tasa_enfriamiento': 0.95},
            {'temperatura_inicial': 100.0, 'tasa_enfriamiento': 0.99},
            {'temperatura_inicial': 50.0,  'tasa_enfriamiento': 0.80}
        ]),
        
        ("Algoritmo 4", BusquedaLocalIterada, [
            {'paso_local': 0.1, 'paso_perturbacion': 1.0, 'iteraciones_locales': 50},
            {'paso_local': 0.5, 'paso_perturbacion': 2.0, 'iteraciones_locales': 50},
            {'paso_local': 0.1, 'paso_perturbacion': 5.0, 'iteraciones_locales': 100},
            {'paso_local': 1.0, 'paso_perturbacion': 2.0, 'iteraciones_locales': 20}
        ]),
        
        ("Algoritmo 5", BusquedaVecindadVariable, [
            {'vecindarios': [0.1, 0.5, 1.0]},
            {'vecindarios': [0.1, 1.0, 2.0, 5.0]},
            {'vecindarios': [0.5, 2.0, 4.0]},
            {'vecindarios': [0.01, 0.1, 0.5, 1.0]}
        ])
    ]

    print("\n" + "*" * 65)
    print("  INICIANDO FRAMEWORK DE OPTIMIZACIÓN HEURÍSTICA - LAB 7")
    print("  (4 Funciones x 5 Algoritmos | Presupuesto: 10.000 llamadas)")
    print("*" * 65 + "\n")

    # Diccionarios para guardar resultados
    resultados_valores = {}
    resultados_vectores = {}

    print("Calculando... (Esto tardará unos segundos)\n")

    # BUCLE PRINCIPAL
    for nombre_func, ClaseFuncion in funciones_a_evaluar:
        print(f"> Procesando CAJA NEGRA: {nombre_func.upper()} ...")
        
        resultados_valores[nombre_func] = []
        resultados_vectores[nombre_func] = []
        
        for nombre_alg, ClaseAlgoritmo, grid in configuraciones_algoritmos:
            funcion_actual = ClaseFuncion()
            funcion_actual.reiniciar_contador()
            algoritmo = ClaseAlgoritmo()
            
            # --- FASE 1: GRID SEARCH ---
            if grid:
                evaluaciones_por_prueba = PRESUPUESTO_GRID // len(grid)
                algoritmo.grid_search(funcion_actual, grid, evaluaciones_por_prueba)

            # --- FASE 2: ATAQUE FINAL ---
            mejor_x, mejor_valor = algoritmo.ejecutar(funcion_actual, PRESUPUESTO_TOTAL)
            
            # Guardamos el valor
            resultados_valores[nombre_func].append(mejor_valor)
            
            # Guardamos el vector formateado con espaciado
            vector_compacto = "[" + ", ".join([f"{v:5.1f}" for v in mejor_x]) + "]"
            resultados_vectores[nombre_func].append(vector_compacto)

    print("\n¡Cálculos terminados!\n")

    # ==========================================
    # TABLA 1: VALORES MÍNIMOS (Horizontal, centrada)
    # ==========================================
    print("=" * 105)
    print(f"{'TABLA 1: VALORES MÍNIMOS ENCONTRADOS (LAB 7)':^105}")
    print("=" * 105)
    print(f"{'FUNCIÓN':<15} | {'Algoritmo 1':^15} | {'Algoritmo 2':^15} | {'Algoritmo 3':^15} | {'Algoritmo 4':^15} | {'Algoritmo 5':^15}")
    print("-" * 105)
    
    for nombre_func, valores in resultados_valores.items():
        v_str = [f"{v:.4f}" for v in valores]
        print(f"{nombre_func:<15} | {v_str[0]:^15} | {v_str[1]:^15} | {v_str[2]:^15} | {v_str[3]:^15} | {v_str[4]:^15}")

    print("\n\n")

    # ==========================================
    # TABLA 2: VECTORES MÍNIMOS (Vertical por función)
    # ==========================================
    print("=" * 80)
    print(f"{'TABLA 2: VECTORES ÓPTIMOS (FENOTIPOS)':^80}")
    print("=" * 80)
    
    nombres_algoritmos = [alg[0] for alg in configuraciones_algoritmos]
    
    for nombre_func, vectores in resultados_vectores.items():
        print(f"\n[ CAJA NEGRA: {nombre_func.upper()} ]")
        print("-" * 40)
        for i, nombre_alg in enumerate(nombres_algoritmos):
            print(f"  {nombre_alg:<15} ->  {vectores[i]}")

    print("\n" + "*" * 80)
    print(f"{'FIN DEL LABORATORIO 7':^80}")
    print("*" * 80 + "\n")