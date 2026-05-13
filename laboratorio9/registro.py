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
        """Devuelve una LISTA de atributos normalizada."""
        if len(self.atributos) != len(minimos) or len(self.atributos) != len(maximos):
            raise ValueError(f"Discrepancia: {len(self.atributos)} attrs vs {len(minimos)} min/max.")
        
        return [(x - mi) / (ma - mi) if ma != mi else 0.0 
                for x, mi, ma in zip(self.atributos, minimos, maximos)]

    def estandarizar(self, medias, desviaciones):
        if len(self.atributos) != len(medias) or len(self.atributos) != len(desviaciones):
            # Cambiamos el raise por un mensaje informativo para depurar si falla
            raise ValueError(f"Dim: {len(self.atributos)} attrs vs {len(medias)} medias")
            
        return [(x - m) / d if d > 0.0000001 else 0.0 
                for x, m, d in zip(self.atributos, medias, desviaciones)]

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