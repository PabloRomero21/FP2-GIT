import math
import numpy as np
import retos_optimizacion as reto
if __name__ == "__main__":
    valor=[0]*10
    f1 = reto.Funcion_1()
    f2 = reto.Funcion_2()
    f3 = reto.Funcion_3()
    f4 = reto.Funcion_4()
    print(f"Función 1 en cero vale: {f1.evaluar(valor):.4f}")
    print(f"Función 2 en cero vale: {f2.evaluar(valor):.4f}")
    print(f"Función 3 en cero vale: {f3.evaluar(valor):.4f}")
    print(f"Función 4 en cero vale: {f4.evaluar(valor):.4f}")
          
