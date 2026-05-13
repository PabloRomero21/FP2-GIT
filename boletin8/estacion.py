# estacion.py
import math

# 1. La clase Coordenada (la ponemos aquí para no crear más archivos)
class Coordenada:
    def __init__(self, latitud, longitud):
        self.latitud = latitud
        self.longitud = longitud

    def distancia_haversine(self, otra):
        """Calcula la distancia en km usando la fórmula de Haversine."""
        R = 6371.0
        phi1, phi2 = math.radians(self.latitud), math.radians(otra.latitud)
        delta_phi = math.radians(otra.latitud - self.latitud)
        delta_lambda = math.radians(otra.longitud - self.longitud)

        a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

# 2. La clase Estacion
class Estacion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.lineas = set()
        self.coordenada = None  # <-- Aquí guardaremos el objeto Coordenada

    def agregar_linea(self, nombre_linea):
        self.lineas.add(nombre_linea)

    def asignar_coordenada(self, lat, lon):
        """Crea un objeto Coordenada y se lo asigna a la estación."""
        self.coordenada = Coordenada(lat, lon)

    def __eq__(self, otro):
        if not isinstance(otro, Estacion): return False
        return self.nombre == otro.nombre and self.lineas == otro.lineas

# 3. La clase Estaciones (Colección)
class Estaciones:
    def __init__(self):
        self.coleccion = {}

    def agregar_estacion(self, estacion):
        self.coleccion[estacion.nombre] = estacion

    def __eq__(self, otro):
        if not isinstance(otro, Estaciones): return False
        return self.coleccion == otro.coleccion

    def a_lineas(self):
        from linea import Linea, Lineas
        nuevas_lineas = Lineas()
        for estacion in self.coleccion.values():
            for nombre_linea in estacion.lineas:
                if nombre_linea not in nuevas_lineas.coleccion:
                    nuevas_lineas.agregar_linea(Linea(nombre_linea))
                nuevas_lineas.coleccion[nombre_linea].agregar_parada(estacion.nombre)
        return nuevas_lineas

    # --- MÉTODO PARA BUSCAR LA ESTACIÓN MÁS CERCANA ---
    def estacion_mas_cercana(self, lat_comercio, lon_comercio):
        punto_referencia = Coordenada(lat_comercio, lon_comercio)
        estacion_mas_cercana = None
        distancia_minima = float('inf')

        for estacion in self.coleccion.values():
            if estacion.coordenada is not None:  # Solo comprobamos las que tienen coordenada
                d = punto_referencia.distancia_haversine(estacion.coordenada)
                if d < distancia_minima:
                    distancia_minima = d
                    estacion_mas_cercana = estacion
        
        return estacion_mas_cercana, distancia_minima

    # --- MÉTODOS DEL GRAFO QUE YA TENÍAMOS ---
    def estaciones_con_mas_lineas(self):
        if not self.coleccion: return [], 0
        max_lineas = 0
        estaciones_top = []
        for estacion in self.coleccion.values():
            num_lineas = len(estacion.lineas)
            if num_lineas > max_lineas:
                max_lineas = num_lineas
                estaciones_top = [estacion.nombre]
            elif num_lineas == max_lineas:
                estaciones_top.append(estacion.nombre)
        return estaciones_top, max_lineas

    def comparten_linea(self, nombre_estacion1, nombre_estacion2):
        if nombre_estacion1 not in self.coleccion or nombre_estacion2 not in self.coleccion:
            return False
        estacion1 = self.coleccion[nombre_estacion1]
        estacion2 = self.coleccion[nombre_estacion2]
        lineas_comunes = estacion1.lineas.intersection(estacion2.lineas)
        return len(lineas_comunes) > 0

    def eliminar_linea(self, nombre_linea):
        for estacion in self.coleccion.values():
            estacion.lineas.discard(nombre_linea)

    def es_conexo(self):
        if not self.coleccion: return True
        lineas_a_estaciones = {}
        for estacion in self.coleccion.values():
            for linea in estacion.lineas:
                if linea not in lineas_a_estaciones:
                    lineas_a_estaciones[linea] = []
                lineas_a_estaciones[linea].append(estacion)
        estacion_inicio = next(iter(self.coleccion.values()))
        visitadas = set([estacion_inicio.nombre])
        cola = [estacion_inicio]
        while cola:
            actual = cola.pop(0)
            for linea in actual.lineas:
                if linea in lineas_a_estaciones:
                    for vecina in lineas_a_estaciones[linea]:
                        if vecina.nombre not in visitadas:
                            visitadas.add(vecina.nombre)
                            cola.append(vecina)
        return len(visitadas) == len(self.coleccion)
    

    def trayecto_directo(self, origen, destino):
        """Devuelve las líneas que conectan dos estaciones directamente."""
        if origen not in self.coleccion or destino not in self.coleccion:
            return set()
        # Intersección de los conjuntos de líneas
        return self.coleccion[origen].lineas.intersection(self.coleccion[destino].lineas)

    def trayecto_un_transbordo(self, origen, destino):
        """Busca estaciones de transbordo entre dos puntos."""
        posibles_rutas = []
        lineas_origen = self.coleccion[origen].lineas
        lineas_destino = self.coleccion[destino].lineas

        # Recorremos todas las estaciones de la red buscando una que sirva de puente
        for nombre_intermedia, est_intermedia in self.coleccion.items():
            if nombre_intermedia == origen or nombre_intermedia == destino:
                continue
            
            # ¿Esta estación intermedia conecta con mi origen y mi destino?
            interseccion_origen = lineas_origen.intersection(est_intermedia.lineas)
            interseccion_destino = lineas_destino.intersection(est_intermedia.lineas)
            
            if interseccion_origen and interseccion_destino:
                posibles_rutas.append({
                    "estacion_cambio": nombre_intermedia,
                    "linea_1": list(interseccion_origen)[0],
                    "linea_2": list(interseccion_destino)[0]
                })
        return posibles_rutas

    def ruta_optima_general(self, inicio, fin):
        """Algoritmo BFS para encontrar la ruta con menos estaciones entre dos puntos."""
        if inicio not in self.coleccion or fin not in self.coleccion:
            return None

        # Cola para el BFS: guarda (estacion_actual, camino_recorrido)
        cola = [(inicio, [inicio])]
        visitados = {inicio}

        # Necesitamos saber qué estaciones hay en cada línea (lo calculamos rápido)
        lineas_map = {}
        for est in self.coleccion.values():
            for l in est.lineas:
                if l not in lineas_map: lineas_map[l] = []
                lineas_map[l].append(est.nombre)

        while cola:
            (actual, camino) = cola.pop(0)
            
            # Exploramos vecinos (estaciones en las mismas líneas)
            for nombre_linea in self.coleccion[actual].lineas:
                for vecino in lineas_map[nombre_linea]:
                    if vecino == fin:
                        return camino + [vecino]
                    if vecino not in visitados:
                        visitados.add(vecino)
                        cola.append((vecino, camino + [vecino]))
        return None
    

    def contar_estaciones_aisladas(self, nombre_linea_a_eliminar):
        if not self.coleccion:
            return 0

        # 1. Identificar la estación de inicio (el "núcleo")
        estacion_inicio = next(iter(self.coleccion.values()))
        
        # 2. Exploración BFS
        visitadas = {estacion_inicio.nombre} # Usamos nombres únicos
        cola = [estacion_inicio]

        while cola:
            actual = cola.pop(0)
            for nombre_linea in actual.lineas:
                # Solo seguimos el camino si NO es la línea que hemos quitado
                if nombre_linea != nombre_linea_a_eliminar:
                    # Buscamos qué otras estaciones tienen esa línea
                    for posible_vecina in self.coleccion.values():
                        if nombre_linea in posible_vecina.lineas:
                            if posible_vecina.nombre not in visitadas:
                                visitadas.add(posible_vecina.nombre)
                                cola.append(posible_vecina)

        # 3. El cálculo final:*
        # Total de estaciones únicas - estaciones que siguen conectadas
        total_reales = len(self.coleccion)
        conectadas = len(visitadas)
        
        return total_reales - conectadas
    
    def obtener_total_estaciones(self):
        """Devuelve el número total de estaciones físicas (sin duplicados)."""
        # len() sobre el diccionario devuelve el número de llaves únicas (nombres de estaciones)
        return len(self.coleccion)