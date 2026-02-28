import math

class Registro:
    def __init__(self, atributos):
        """Constructor de la clase Registro."""
        self.atributos = [float(x) for x in atributos]

    def distancia_euclidea(self, otro):
        """Calcula la distancia Euclídea entre dos Registros."""
        if len(self.atributos) != len(otro.atributos):
            raise ValueError("Los registros deben tener la misma dimensión.")
        suma_cuadrados = sum((a - b) ** 2 for a, b in zip(self.atributos, otro.atributos))
        return math.sqrt(suma_cuadrados)

    def distancia_manhattan(self, otro):
        """Calcula la distancia Manhattan entre dos Registros."""
        if len(self.atributos) != len(otro.atributos):
            raise ValueError("Los registros deben tener la misma dimensión.")
        return sum(abs(a - b) for a, b in zip(self.atributos, otro.atributos))

    def distancia_ponderada(self, otro, pesos):
        """Calcula la distancia ponderada entre dos Registros."""
        if len(self.atributos) != len(otro.atributos) or len(self.atributos) != len(pesos):
            raise ValueError("Dimensiones incompatibles entre registros o pesos.")
        suma_ponderada = sum(w * (a - b)**2 for w, a, b in zip(pesos, self.atributos, otro.atributos))
        return math.sqrt(suma_ponderada)

    def calcula_distancia(self, otro, tipo="euclídea", pesos=None):
        """Selector centralizado de distancias."""
        if tipo == "euclídea":
            return self.distancia_euclidea(otro)
        elif tipo == "manhattan":
            return self.distancia_manhattan(otro)
        elif tipo == "ponderada":
            if pesos is None:
                raise ValueError("Se requieren pesos para la distancia ponderada.")
            return self.distancia_ponderada(otro, pesos)
        else:
            raise ValueError(f"Tipo '{tipo}' no reconocido.")

    def normalizar(self, minimos, maximos):
        """Devuelve un NUEVO objeto normalizado [0, 1] de la clase correspondiente."""
        if len(self.atributos) != len(minimos) or len(self.atributos) != len(maximos):
            raise ValueError("Las listas de min/max deben coincidir.")
        
        nuevos_atributos = []
        for x, mi, ma in zip(self.atributos, minimos, maximos):
            valor_norm = (x - mi) / (ma - mi) if ma != mi else 0.0
            nuevos_atributos.append(valor_norm)
        
        # --- EL CAMBIO CLAVE DE POO ---
        # Comprobamos si el objeto que invoca tiene el atributo 'objetivo'
        if hasattr(self, 'objetivo'):
            # Si es Clasificacion o Regresion, pasamos los atributos y su objetivo
            return self.__class__(nuevos_atributos, self.objetivo)
        else:
            # Si es un Registro base puro, solo pasamos los atributos
            return self.__class__(nuevos_atributos)

    def k_vecinos(self, lista_registros, k, tipo="euclídea", pesos=None):
        """Encuentra los índices de los k registros más cercanos."""
        distancias_con_indice = []
        for i, registro_externo in enumerate(lista_registros):
            dist = self.calcula_distancia(registro_externo, tipo, pesos)
            distancias_con_indice.append((dist, i))
            
        distancias_con_indice.sort(key=lambda x: x[0])
        return [item[1] for item in distancias_con_indice[:k]]

    def __repr__(self):
        # Mostramos los valores redondeados para una lectura limpia en consola
        vals = [round(a, 3) for a in self.atributos]
        return f"Registro({vals})"
    
class RegistroClasificacion(Registro):
    def __init__(self, atributos, objetivo):
        super().__init__(atributos)
        self.objetivo = str(objetivo) # Etiqueta de texto

    # ¡Ya no necesitamos redefinir normalizar aquí!

    def __repr__(self):
        repr_padre = super().__repr__()
        return f"{repr_padre} | Objetivo: '{self.objetivo}'"


class RegistroRegresion(Registro):
    def __init__(self, atributos, objetivo):
        super().__init__(atributos)
        # Convertimos explícitamente a float porque el objetivo es un valor real
        self.objetivo = float(objetivo) 

    # Tampoco necesitamos redefinir normalizar aquí gracias al polimorfismo

    def __repr__(self):
        repr_padre = super().__repr__()
        return f"{repr_padre} | Objetivo: {self.objetivo}"