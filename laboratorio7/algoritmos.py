import numpy as np

class AlgoritmoOptimizacion:
    """
    Clase base para todos los algoritmos de optimización.
    Contiene la configuración común y métodos de utilidad.
    """
    def __init__(self, dimensiones=10, limite_inferior=-10, limite_superior=10):
        self.dimensiones = dimensiones
        self.limite_inferior = limite_inferior
        self.limite_superior = limite_superior

    def generar_punto_aleatorio(self):
        """Genera un array de números aleatorios dentro de los límites."""
        return np.random.uniform(
            self.limite_inferior, 
            self.limite_superior, 
            self.dimensiones
        )
    

    def grid_search(self, funcion, combinaciones_parametros, evaluaciones_por_prueba):
        """
        Prueba diferentes configuraciones y se queda con la mejor.
        'combinaciones_parametros' es una lista de diccionarios.
        """
        # Si es un algoritmo sin parámetros (como la Búsqueda Aleatoria), no hacemos nada
        if not combinaciones_parametros:
            return None

        mejor_resultado = float('inf')
        mejores_parametros = None

        for parametros in combinaciones_parametros:
            # 1. Inyectamos los parámetros al algoritmo (Ej: se le pone la temperatura o el paso)
            for clave, valor in parametros.items():
                setattr(self, clave, valor)

            # 2. Calculamos el presupuesto para esta prueba concreta
            limite_evaluaciones = funcion.presupuesto_gastado + evaluaciones_por_prueba

            # 3. Lanzamos el algoritmo "de prueba" y vemos hasta dónde baja
            _, valor_obtenido = self.ejecutar(funcion, limite_evaluaciones)

            # 4. Comprobamos si esta configuración es la campeona hasta ahora
            if valor_obtenido < mejor_resultado:
                mejor_resultado = valor_obtenido
                mejores_parametros = parametros.copy()

        # 5. MUY IMPORTANTE: Dejamos el algoritmo configurado con los parámetros ganadores 
        # para que estén listos de cara a la ejecución final
        for clave, valor in mejores_parametros.items():
            setattr(self, clave, valor)

        return mejores_parametros
    
    

    def ejecutar(self, funcion, max_evaluaciones):
        """
        Método principal que deberán sobrescribir las clases hijas.
        """
        raise NotImplementedError("Este método debe ser implementado por el algoritmo específico.")


class BusquedaAleatoria(AlgoritmoOptimizacion):
    """Algoritmo 1: Búsqueda Aleatoria Pura"""
    
    # No necesitamos un __init__ propio porque usamos el del padre
    
    def ejecutar(self, funcion, max_evaluaciones):
        mejor_x = self.generar_punto_aleatorio()
        mejor_valor = funcion.evaluar(mejor_x) 
        
        while funcion.presupuesto_gastado < max_evaluaciones:
            candidato_x = self.generar_punto_aleatorio()
            valor_candidato = funcion.evaluar(candidato_x)
            
            if valor_candidato < mejor_valor:
                mejor_valor = valor_candidato
                mejor_x = candidato_x
                
        return mejor_x, mejor_valor


class HillClimbing(AlgoritmoOptimizacion):
    """Algoritmo 2: Ascenso de Colinas (Hill Climbing)"""
    
    def __init__(self, tamano_paso=0.5, dimensiones=10, limite_inferior=-10, limite_superior=10):
        # Llamamos al constructor del padre para inicializar dimensiones y límites
        super().__init__(dimensiones, limite_inferior, limite_superior)
        # Añadimos el parámetro específico de este algoritmo
        self.tamano_paso = tamano_paso
        
    def ejecutar(self, funcion, max_evaluaciones):
        mejor_x = self.generar_punto_aleatorio()
        mejor_valor = funcion.evaluar(mejor_x)
        
        while funcion.presupuesto_gastado < max_evaluaciones:
            ruido = np.random.normal(0, self.tamano_paso, self.dimensiones)
            candidato_x = mejor_x + ruido
            
            # Aseguramos que no se salga de los límites [-10, 10]
            candidato_x = np.clip(candidato_x, self.limite_inferior, self.limite_superior)
            
            valor_candidato = funcion.evaluar(candidato_x)
            
            if valor_candidato < mejor_valor:
                mejor_valor = valor_candidato
                mejor_x = candidato_x
                
        return mejor_x, mejor_valor
    

class RecocidoSimulado(AlgoritmoOptimizacion):
    """Algoritmo 3: Recocido Simulado (Simulated Annealing)"""
    
    def __init__(self, temperatura_inicial=100.0, tasa_enfriamiento=0.99, tamano_paso=0.5, dimensiones=10, limite_inferior=-10, limite_superior=10):
        super().__init__(dimensiones, limite_inferior, limite_superior)
        self.temperatura_inicial = temperatura_inicial
        self.tasa_enfriamiento = tasa_enfriamiento
        self.tamano_paso = tamano_paso
        
    def ejecutar(self, funcion, max_evaluaciones):
        mejor_x = self.generar_punto_aleatorio()
        mejor_valor = funcion.evaluar(mejor_x)
        
        # El recocido guarda el "estado actual", que no siempre es el "mejor global"
        x_actual = mejor_x.copy()
        valor_actual = mejor_valor
        temperatura = self.temperatura_inicial
        
        while funcion.presupuesto_gastado < max_evaluaciones:
            ruido = np.random.normal(0, self.tamano_paso, self.dimensiones)
            candidato_x = x_actual + ruido
            candidato_x = np.clip(candidato_x, self.limite_inferior, self.limite_superior)
            
            valor_candidato = funcion.evaluar(candidato_x)
            
            # Calculamos la diferencia (si es negativa, es que hemos mejorado)
            diferencia = valor_candidato - valor_actual
            
            # ¿Aceptamos el nuevo paso?
            # 1. Si mejora (diferencia < 0), lo aceptamos siempre.
            # 2. Si empeora, lo aceptamos con una probabilidad que depende de la Temperatura
            if diferencia < 0 or np.random.rand() < np.exp(-diferencia / temperatura):
                x_actual = candidato_x
                valor_actual = valor_candidato
                
                # Si además de aceptarlo, resulta ser el mejor de TODA la historia, lo guardamos
                if valor_candidato < mejor_valor:
                    mejor_valor = valor_candidato
                    mejor_x = candidato_x.copy()
                    
            # Enfriamos un poquito la temperatura para el siguiente ciclo
            temperatura *= self.tasa_enfriamiento
            
            # Evitamos que la temperatura llegue a 0 absoluto para no dividir por 0
            temperatura = max(temperatura, 1e-8)
                
        return mejor_x, mejor_valor
    


class BusquedaLocalIterada(AlgoritmoOptimizacion):
    """Algoritmo 4: Búsqueda Local Iterada (Iterated Local Search - ILS)"""
    
    def __init__(self, paso_local=0.1, paso_perturbacion=2.0, iteraciones_locales=50, dimensiones=10, limite_inferior=-10, limite_superior=10):
        super().__init__(dimensiones, limite_inferior, limite_superior)
        self.paso_local = paso_local
        self.paso_perturbacion = paso_perturbacion
        self.iteraciones_locales = iteraciones_locales
        
    def ejecutar(self, funcion, max_evaluaciones):
        mejor_x_global = self.generar_punto_aleatorio()
        mejor_valor_global = funcion.evaluar(mejor_x_global)
        
        while funcion.presupuesto_gastado < max_evaluaciones:
            # 1. Perturbación (Damos un salto grande desde el mejor global conocido)
            # (No lo hacemos en la primerísima vuelta para aprovechar el punto aleatorio puro)
            if funcion.presupuesto_gastado > 1:
                ruido_fuerte = np.random.normal(0, self.paso_perturbacion, self.dimensiones)
                x_actual = mejor_x_global + ruido_fuerte
                x_actual = np.clip(x_actual, self.limite_inferior, self.limite_superior)
                valor_actual = funcion.evaluar(x_actual)
            else:
                x_actual = mejor_x_global.copy()
                valor_actual = mejor_valor_global

            # Control de seguridad por si la perturbación gastó el último intento
            if funcion.presupuesto_gastado >= max_evaluaciones: 
                break

            # 2. Búsqueda Local (Hacemos un Hill Climbing cortito desde el nuevo punto)
            evaluaciones_inicio_local = funcion.presupuesto_gastado
            while (funcion.presupuesto_gastado - evaluaciones_inicio_local) < self.iteraciones_locales and funcion.presupuesto_gastado < max_evaluaciones:
                ruido_suave = np.random.normal(0, self.paso_local, self.dimensiones)
                candidato_x = x_actual + ruido_suave
                candidato_x = np.clip(candidato_x, self.limite_inferior, self.limite_superior)
                
                valor_candidato = funcion.evaluar(candidato_x)
                
                if valor_candidato < valor_actual:
                    valor_actual = valor_candidato
                    x_actual = candidato_x
                    
            # 3. ¿Hemos superado al mejor global de todos los tiempos?
            if valor_actual < mejor_valor_global:
                mejor_valor_global = valor_actual
                mejor_x_global = x_actual.copy()
                
        return mejor_x_global, mejor_valor_global


class BusquedaVecindadVariable(AlgoritmoOptimizacion):
    """Algoritmo 5: Búsqueda de Vecindad Variable Continua (VNS)"""
    
    def __init__(self, vecindarios=[0.1, 0.5, 1.0, 2.0, 5.0], dimensiones=10, limite_inferior=-10, limite_superior=10):
        super().__init__(dimensiones, limite_inferior, limite_superior)
        self.vecindarios = vecindarios
        
    def ejecutar(self, funcion, max_evaluaciones):
        mejor_x = self.generar_punto_aleatorio()
        mejor_valor = funcion.evaluar(mejor_x)
        
        k = 0 # Índice del tamaño de paso actual
        
        while funcion.presupuesto_gastado < max_evaluaciones:
            tamano_paso = self.vecindarios[k]
            
            ruido = np.random.normal(0, tamano_paso, self.dimensiones)
            candidato_x = mejor_x + ruido
            candidato_x = np.clip(candidato_x, self.limite_inferior, self.limite_superior)
            
            valor_candidato = funcion.evaluar(candidato_x)
            
            if valor_candidato < mejor_valor:
                # Si mejoramos, guardamos y volvemos al paso más pequeño (k=0) para afinar
                mejor_valor = valor_candidato
                mejor_x = candidato_x
                k = 0 
            else:
                # Si no mejoramos, pasamos al siguiente tamaño de paso (más grande)
                k = (k + 1) % len(self.vecindarios)
                
        return mejor_x, mejor_valor