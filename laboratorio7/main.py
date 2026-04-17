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

    # Lista con las 4 funciones ofuscadas (usamos sus clases para instanciarlas en cada vuelta)
    funciones_a_evaluar = [
        reto.Funcion_1, 
        reto.Funcion_2, 
        reto.Funcion_3, 
        reto.Funcion_4
    ]

    # Diccionario/Lista de algoritmos con su "Cuadrícula" (Grid) de parámetros a probar
    # Fíjate cómo cada algoritmo tiene 4 configuraciones diferentes para probar
    configuraciones_algoritmos = [
        ("Búsqueda Aleatoria", BusquedaAleatoria, []), # No tiene parámetros
        
        ("Hill Climbing", HillClimbing, [
            {'tamano_paso': 0.1}, 
            {'tamano_paso': 0.5}, 
            {'tamano_paso': 1.5}, 
            {'tamano_paso': 3.0}
        ]),
        
        ("Recocido Simulado", RecocidoSimulado, [
            {'temperatura_inicial': 100.0, 'tasa_enfriamiento': 0.90},
            {'temperatura_inicial': 1000.0, 'tasa_enfriamiento': 0.95},
            {'temperatura_inicial': 100.0, 'tasa_enfriamiento': 0.99},
            {'temperatura_inicial': 50.0,  'tasa_enfriamiento': 0.80}
        ]),
        
        ("Búsqueda Local Iterada (ILS)", BusquedaLocalIterada, [
            {'paso_local': 0.1, 'paso_perturbacion': 1.0, 'iteraciones_locales': 50},
            {'paso_local': 0.5, 'paso_perturbacion': 2.0, 'iteraciones_locales': 50},
            {'paso_local': 0.1, 'paso_perturbacion': 5.0, 'iteraciones_locales': 100},
            {'paso_local': 1.0, 'paso_perturbacion': 2.0, 'iteraciones_locales': 20}
        ]),
        
        ("Vecindad Variable (VNS)", BusquedaVecindadVariable, [
            {'vecindarios': [0.1, 0.5, 1.0]},
            {'vecindarios': [0.1, 1.0, 2.0, 5.0]},
            {'vecindarios': [0.5, 2.0, 4.0]},
            {'vecindarios': [0.01, 0.1, 0.5, 1.0]}
        ])
    ]

    print("\n" + "*" * 65)
    print("  INICIANDO FRAMEWORK DE OPTIMIZACIÓN HEURÍSTICA - LAB 7")
    print("  (4 Funciones x 5 Algoritmos | Presupuesto: 10.000 llamadas)")
    print("*" * 65)

    # BUCLE PRINCIPAL: Recorremos las 4 cajas negras
    for i, ClaseFuncion in enumerate(funciones_a_evaluar, 1):
        print(f"\n{'='*20} CAJA NEGRA: FUNCIÓN {i} {'='*20}")
        
        # Recorremos los 5 algoritmos para la función actual
        for nombre_alg, ClaseAlgoritmo, grid in configuraciones_algoritmos:
            # Creamos una instancia "limpia" de la función para este algoritmo
            funcion_actual = ClaseFuncion()
            funcion_actual.reiniciar_contador()
            
            # Instanciamos el algoritmo
            algoritmo = ClaseAlgoritmo()
            
            print(f"\n> Ejecutando modelo: {nombre_alg}")
            
            # --- FASE 1: GRID SEARCH ---
            if grid:
                # Dividimos las 2000 llamadas entre las configuraciones (ej: 4 configs = 500 llamadas c/u)
                evaluaciones_por_prueba = PRESUPUESTO_GRID // len(grid)
                mejores_params = algoritmo.grid_search(funcion_actual, grid, evaluaciones_por_prueba)
                print(f"  [+] Grid Search: Los mejores parámetros son -> {mejores_params}")
            else:
                print("  [+] Grid Search: No aplica (Algoritmo sin parámetros)")

            # --- FASE 2: ATAQUE FINAL ---
            # El algoritmo ya se quedó guardado internamente con los 'mejores_params'
            # Le pasamos el tope absoluto de 10000. Como ya gastó 2000, usará exactamente 8000.
            mejor_x, mejor_valor = algoritmo.ejecutar(funcion_actual, PRESUPUESTO_TOTAL)
            
            print(f"  [★] RESULTADO FINAL MÁS BAJO : {mejor_valor:.6f}")
            print(f"  [i] Presupuesto consumido    : {funcion_actual.presupuesto_gastado} / {PRESUPUESTO_TOTAL}")

    print("\n" + "*" * 65)
    print("                EVALUACIÓN COMPLETADA CON ÉXITO")
    print("*" * 65 + "\n")