import numpy as np

class AlgoritmoOptimizacion:
    """Clase base para todos los algoritmos de optimización."""
    def __init__(self, dimensiones=10, limite_inferior=-10, limite_superior=10):
        self.dimensiones = dimensiones
        self.limite_inferior = limite_inferior
        self.limite_superior = limite_superior
        self.historial = []  # Libreta para apuntar el avance

    def generar_punto_aleatorio(self):
        return np.random.uniform(self.limite_inferior, self.limite_superior, self.dimensiones)

    def formatear_vector(self, vector):
        valores_str = ", ".join([f"{v:7.4f}" for v in vector])
        return f"[{valores_str}]"

    def grid_search(self, funcion, combinaciones_parametros, evaluaciones_por_prueba):
        if not combinaciones_parametros:
            return None

        mejor_resultado = float('inf')
        mejores_parametros = None

        for parametros in combinaciones_parametros:
            for clave, valor in parametros.items():
                setattr(self, clave, valor)

            limite_evaluaciones = funcion.presupuesto_gastado + evaluaciones_por_prueba
            _, valor_obtenido = self.ejecutar(funcion, limite_evaluaciones)

            if valor_obtenido < mejor_resultado:
                mejor_resultado = valor_obtenido
                mejores_parametros = parametros.copy()

        for clave, valor in mejores_parametros.items():
            setattr(self, clave, valor)

        return mejores_parametros

    def ejecutar(self, funcion, max_evaluaciones):
        raise NotImplementedError("Implementar en clase hija.")


class BusquedaAleatoria(AlgoritmoOptimizacion):
    def ejecutar(self, funcion, max_evaluaciones):
        self.historial = []
        mejor_x = self.generar_punto_aleatorio()
        mejor_valor = funcion.evaluar(mejor_x)
        self.historial.append(mejor_valor)
        
        while funcion.presupuesto_gastado < max_evaluaciones:
            candidato_x = self.generar_punto_aleatorio()
            valor_candidato = funcion.evaluar(candidato_x)
            
            if valor_candidato < mejor_valor:
                mejor_valor = valor_candidato
                mejor_x = candidato_x
            
            self.historial.append(mejor_valor)
                
        return mejor_x, mejor_valor


class HillClimbing(AlgoritmoOptimizacion):
    def __init__(self, tamano_paso=0.5, dimensiones=10, limite_inferior=-10, limite_superior=10):
        super().__init__(dimensiones, limite_inferior, limite_superior)
        self.tamano_paso = tamano_paso
        
    def ejecutar(self, funcion, max_evaluaciones):
        self.historial = []
        mejor_x = self.generar_punto_aleatorio()
        mejor_valor = funcion.evaluar(mejor_x)
        self.historial.append(mejor_valor)
        
        inicio_presupuesto = funcion.presupuesto_gastado 
        evaluaciones_totales = max_evaluaciones - inicio_presupuesto
        
        while funcion.presupuesto_gastado < max_evaluaciones:
            # Paso dinámico que decrece con el tiempo
            progreso = (funcion.presupuesto_gastado - inicio_presupuesto) / evaluaciones_totales
            factor = max(1.0 - progreso, 0.01) 
            
            ruido = np.random.normal(0, self.tamano_paso * factor, self.dimensiones)
            candidato_x = np.clip(mejor_x + ruido, self.limite_inferior, self.limite_superior)
            valor_candidato = funcion.evaluar(candidato_x)
            
            if valor_candidato < mejor_valor:
                mejor_valor = valor_candidato
                mejor_x = candidato_x
            
            self.historial.append(mejor_valor)
                
        return mejor_x, mejor_valor


class RecocidoSimulado(AlgoritmoOptimizacion):
    def __init__(self, temperatura_inicial=100.0, tasa_enfriamiento=0.99, tamano_paso=0.5, dimensiones=10, limite_inferior=-10, limite_superior=10):
        super().__init__(dimensiones, limite_inferior, limite_superior)
        self.temperatura_inicial = temperatura_inicial
        self.tasa_enfriamiento = tasa_enfriamiento
        self.tamano_paso = tamano_paso
        
    def ejecutar(self, funcion, max_evaluaciones):
        self.historial = []
        mejor_x = self.generar_punto_aleatorio()
        mejor_valor = funcion.evaluar(mejor_x)
        
        x_actual = mejor_x.copy()
        valor_actual = mejor_valor
        temperatura = self.temperatura_inicial
        self.historial.append(mejor_valor)
        
        inicio_presupuesto = funcion.presupuesto_gastado
        evaluaciones_totales = max_evaluaciones - inicio_presupuesto
        
        while funcion.presupuesto_gastado < max_evaluaciones:
            progreso = (funcion.presupuesto_gastado - inicio_presupuesto) / evaluaciones_totales
            factor = max(1.0 - progreso, 0.01)
            
            ruido = np.random.normal(0, self.tamano_paso * factor, self.dimensiones)
            candidato_x = np.clip(x_actual + ruido, self.limite_inferior, self.limite_superior)
            valor_candidato = funcion.evaluar(candidato_x)
            
            diferencia = valor_candidato - valor_actual
            if diferencia < 0 or np.random.rand() < np.exp(-diferencia / temperatura):
                x_actual = candidato_x
                valor_actual = valor_candidato
                if valor_candidato < mejor_valor:
                    mejor_valor = valor_candidato
                    mejor_x = candidato_x.copy()
                    
            temperatura *= self.tasa_enfriamiento
            temperatura = max(temperatura, 1e-8)
            self.historial.append(mejor_valor)
                
        return mejor_x, mejor_valor


class BusquedaLocalIterada(AlgoritmoOptimizacion):
    def __init__(self, paso_local=0.1, paso_perturbacion=2.0, iteraciones_locales=50, dimensiones=10, limite_inferior=-10, limite_superior=10):
        super().__init__(dimensiones, limite_inferior, limite_superior)
        self.paso_local = paso_local
        self.paso_perturbacion = paso_perturbacion
        self.iteraciones_locales = iteraciones_locales
        
    def ejecutar(self, funcion, max_evaluaciones):
        self.historial = []
        mejor_x_global = self.generar_punto_aleatorio()
        mejor_valor_global = funcion.evaluar(mejor_x_global)
        self.historial.append(mejor_valor_global)
        
        inicio_presupuesto = funcion.presupuesto_gastado
        evaluaciones_totales = max_evaluaciones - inicio_presupuesto
        
        while funcion.presupuesto_gastado < max_evaluaciones:
            progreso = (funcion.presupuesto_gastado - inicio_presupuesto) / evaluaciones_totales
            factor = max(1.0 - progreso, 0.1)
            
            if funcion.presupuesto_gastado > 1:
                ruido_fuerte = np.random.normal(0, self.paso_perturbacion * factor, self.dimensiones)
                x_actual = np.clip(mejor_x_global + ruido_fuerte, self.limite_inferior, self.limite_superior)
                valor_actual = funcion.evaluar(x_actual)
                self.historial.append(mejor_valor_global)
            else:
                x_actual = mejor_x_global.copy()
                valor_actual = mejor_valor_global

            if funcion.presupuesto_gastado >= max_evaluaciones: 
                break

            eval_inicio_local = funcion.presupuesto_gastado
            while (funcion.presupuesto_gastado - eval_inicio_local) < self.iteraciones_locales and funcion.presupuesto_gastado < max_evaluaciones:
                ruido_suave = np.random.normal(0, self.paso_local * factor, self.dimensiones)
                candidato_x = np.clip(x_actual + ruido_suave, self.limite_inferior, self.limite_superior)
                valor_candidato = funcion.evaluar(candidato_x)
                
                if valor_candidato < valor_actual:
                    valor_actual = valor_candidato
                    x_actual = candidato_x
                
                self.historial.append(mejor_valor_global)

            if valor_actual < mejor_valor_global:
                mejor_valor_global = valor_actual
                mejor_x_global = x_actual.copy()
                
        return mejor_x_global, mejor_valor_global


class BusquedaVecindadVariable(AlgoritmoOptimizacion):
    def __init__(self, vecindarios=[0.1, 0.5, 1.0, 2.0, 5.0], dimensiones=10, limite_inferior=-10, limite_superior=10):
        super().__init__(dimensiones, limite_inferior, limite_superior)
        self.vecindarios = vecindarios
        
    def ejecutar(self, funcion, max_evaluaciones):
        self.historial = []
        mejor_x = self.generar_punto_aleatorio()
        mejor_valor = funcion.evaluar(mejor_x)
        self.historial.append(mejor_valor)
        
        k = 0 
        inicio_presupuesto = funcion.presupuesto_gastado
        evaluaciones_totales = max_evaluaciones - inicio_presupuesto
        
        while funcion.presupuesto_gastado < max_evaluaciones:
            progreso = (funcion.presupuesto_gastado - inicio_presupuesto) / evaluaciones_totales
            factor = max(1.0 - progreso, 0.05)
            
            tamano_paso = self.vecindarios[k] * factor
            ruido = np.random.normal(0, tamano_paso, self.dimensiones)
            candidato_x = np.clip(mejor_x + ruido, self.limite_inferior, self.limite_superior)
            valor_candidato = funcion.evaluar(candidato_x)
            
            if valor_candidato < mejor_valor:
                mejor_valor = valor_candidato
                mejor_x = candidato_x
                k = 0 
            else:
                k = (k + 1) % len(self.vecindarios)
            
            self.historial.append(mejor_valor)
                
        return mejor_x, mejor_valor