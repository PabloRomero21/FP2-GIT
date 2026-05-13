# linea.py

class Linea:
    def __init__(self, nombre):
        self.nombre = nombre
        self.paradas = []  # Lista para mantener el orden

    def agregar_parada(self, nombre_estacion):
        self.paradas.append(nombre_estacion)

    def __eq__(self, otro):
        """Comprueba igualdad de datos."""
        if not isinstance(otro, Linea): return False
        return self.nombre == otro.nombre and set(self.paradas) == set(otro.paradas)
    

    def es_circular(self):
        """Devuelve True si la línea empieza y termina en la misma estación."""
        # Comprobamos que haya al menos 2 paradas para evitar errores
        if len(self.paradas) > 1:
            return self.paradas[0] == self.paradas[-1]
        return False

class Lineas:
    def __init__(self):
        self.coleccion = {}  # Diccionario {nombre_linea: objeto Linea}

    def agregar_linea(self, linea):
        self.coleccion[linea.nombre] = linea

    def __eq__(self, otro):
        if not isinstance(otro, Lineas): return False
        return self.coleccion == otro.coleccion

    def a_estaciones(self):
        """Construye un objeto Estaciones a partir de las líneas."""
        # Importación local para evitar 'importación circular' con estacion.py
        from estacion import Estacion, Estaciones 
        
        nuevas_estaciones = Estaciones()
        for linea in self.coleccion.values():
            for parada in linea.paradas:
                if parada not in nuevas_estaciones.coleccion:
                    nuevas_estaciones.agregar_estacion(Estacion(parada))
                nuevas_estaciones.coleccion[parada].agregar_linea(linea.nombre)
        
        return nuevas_estaciones