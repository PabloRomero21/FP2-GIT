import numpy as np
import retos_optimizacion as reto
from funcion_8 import Funcion_8

from algoritmos import (
    BusquedaAleatoria, 
    HillClimbing, 
    RecocidoSimulado, 
    BusquedaLocalIterada, 
    BusquedaVecindadVariable
)

if __name__ == "__main__":
    np.random.seed(1)
    
    PRESUPUESTO_TOTAL = 40000
    PRESUPUESTO_GRID = 4000  

    funciones_a_evaluar = [
        ("funcion_5", reto.Funcion_5), 
        ("funcion_6", reto.Funcion_6), 
        ("funcion_7", reto.Funcion_7),
        ("funcion_8", Funcion_8) 
    ]

    configuraciones_algoritmos = [
        ("Algoritmo 1", BusquedaAleatoria, []),
        ("Algoritmo 2", HillClimbing, [{'tamano_paso': 0.5}, {'tamano_paso': 3.0}]),
        ("Algoritmo 3", RecocidoSimulado, [{'temperatura_inicial': 100.0, 'tasa_enfriamiento': 0.95}]),
        ("Algoritmo 4", BusquedaLocalIterada, [{'paso_local': 0.5, 'paso_perturbacion': 2.0, 'iteraciones_locales': 50}]),
        ("Algoritmo 5", BusquedaVecindadVariable, [{'vecindarios': [0.1, 0.5, 2.0, 5.0]}])
    ]

    print("\n" + "*" * 65)
    print("  INICIANDO FRAMEWORK DE OPTIMIZACIÓN HEURÍSTICA - LAB 8")
    print("  (4 Funciones x 5 Algoritmos | Presupuesto: 40.000 llamadas)")
    print("*" * 65 + "\n")

    resultados_valores = {}
    resultados_vectores = {}

    print("Calculando... (Esto tardará unos segundos con 40.000 iteraciones)\n")

    for nombre_func, ClaseFuncion in funciones_a_evaluar:
        print(f"> Procesando CAJA NEGRA: {nombre_func} ...")
        
        resultados_valores[nombre_func] = []
        resultados_vectores[nombre_func] = []
        
        for nombre_alg, ClaseAlgoritmo, grid in configuraciones_algoritmos:
            funcion_actual = ClaseFuncion()
            funcion_actual.reiniciar_contador()
            algoritmo = ClaseAlgoritmo()
            
            if grid:
                eval_prueba = PRESUPUESTO_GRID // len(grid)
                algoritmo.grid_search(funcion_actual, grid, eval_prueba)

            mejor_x, mejor_valor = algoritmo.ejecutar(funcion_actual, PRESUPUESTO_TOTAL)
            
            resultados_valores[nombre_func].append(mejor_valor)
            
            # Vector un poco más espaciado para que se lea bien en vertical
            vector_compacto = "[" + ", ".join([f"{v:5.1f}" for v in mejor_x]) + "]"
            resultados_vectores[nombre_func].append(vector_compacto)
            
    print("\n¡Cálculos terminados!\n")

    # ==========================================
    # TABLA 1: VALORES MÍNIMOS (Horizontal, centrada)
    # ==========================================
    print("=" * 105)
    print(f"{'TABLA 1: VALORES MÍNIMOS ENCONTRADOS':^105}")
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
            # Imprime el nombre del algoritmo alineado y su vector correspondiente
            print(f"  {nombre_alg:<15} ->  {vectores[i]}")

    print("\n" + "*" * 80)
    print(f"{'FIN DEL LABORATORIO 8':^80}")
    print("*" * 80 + "\n")





