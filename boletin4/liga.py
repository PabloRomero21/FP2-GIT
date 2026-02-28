from equipos import Equipo
from itertools import combinations

class Liga:

    def __init__(self, nombre: str, jugadores_lista: list):
        self.nombre = nombre
        # MEJORA DE RENDIMIENTO: Convertimos la lista en un diccionario
        # Clave: Nombre del jugador | Valor: Objeto Jugador
        self.jugadores = {jugador.nombre: jugador for jugador in jugadores_lista}
        self.equipos = {} 
        self._construir_equipos()

    def _construir_equipos(self):
        """
        Método privado. Recorre todos los jugadores y va creando los objetos
        Equipo e insertando a los jugadores en sus temporadas correspondientes.
        """
        for jugador in self.jugadores.values():
            for est in jugador.estadisticas:
                nombre_equipo = est.equipo
                
                # Si el equipo no existe en el diccionario de la Liga, lo instanciamos
                if nombre_equipo not in self.equipos:
                    self.equipos[nombre_equipo] = Equipo(nombre_equipo)
                    
                # Le decimos al objeto Equipo que guarde a este jugador en esa temporada
                self.equipos[nombre_equipo].agregar_registro(est.temporada, jugador, est)

    def obtener_maximo_goleador_temporada(self):
        max_goles = -1
        mejor_jugador = None
        mejor_estadistica = None

        # Iteramos por los valores del diccionario de jugadores
        for jugador in self.jugadores.values():
            for est in jugador.estadisticas: # Iteramos por los objetos Estadistica
                if est.goles > max_goles:
                    max_goles = est.goles
                    mejor_jugador = jugador
                    mejor_estadistica = est

        # Ahora devolvemos directamente los dos objetos limpios
        return mejor_jugador, mejor_estadistica

    def obtener_maximo_goleador_historico(self):
        max_goles_totales = -1
        mejor_jugador = None

        for jugador in self.jugadores.values():
            # Sumamos el atributo .goles de todos sus objetos Estadistica
            goles_totales = sum(est.goles for est in jugador.estadisticas)
            
            if goles_totales > max_goles_totales:
                max_goles_totales = goles_totales
                mejor_jugador = jugador

        return mejor_jugador, max_goles_totales
    

    def obtener_jugador_mas_equipos(self):
        """
        Busca al jugador (el "trotamundos") que ha jugado en más equipos distintos.
        
        Devuelve: (Objeto Jugador, lista_de_equipos)
        """
        max_equipos = 0
        mejor_jugador = None
        lista_mejores_equipos = []

        for jugador in self.jugadores.values():
            equipos_unicos = []
            
            # Recopilamos los equipos sin repetirlos
            for est in jugador.estadisticas:
                if est.equipo not in equipos_unicos:
                    equipos_unicos.append(est.equipo)
            
            # Si este jugador ha estado en más equipos que el récord actual, lo actualizamos
            if len(equipos_unicos) > max_equipos:
                max_equipos = len(equipos_unicos)
                mejor_jugador = jugador
                lista_mejores_equipos = equipos_unicos

        return mejor_jugador, lista_mejores_equipos


    def obtener_jugador_record_partidos_en_un_club(self):
        """
        Busca al jugador que más partidos ha acumulado vistiendo la misma camiseta.
        Recorre los equipos para sumar las estadísticas de sus jugadores.
        
        Devuelve: (Objeto Jugador, (nombre_equipo, numero_partidos))
        """
        max_partidos = -1
        mejor_jugador = None
        mejor_equipo_nombre = ""

        # Recorremos cada objeto Equipo que tenemos en la Liga
        for equipo_obj in self.equipos.values():
            
            # Para cada equipo, necesitamos sumar los partidos de sus jugadores
            # Usaremos un diccionario temporal: {ObjetoJugador: suma_partidos}
            conteo_jugadores_equipo = {}
            
            for temporada, lista_tuplas in equipo_obj.temporadas.items():
                for jug_obj, est_obj in lista_tuplas:
                    if jug_obj not in conteo_jugadores_equipo:
                        conteo_jugadores_equipo[jug_obj] = 0
                    conteo_jugadores_equipo[jug_obj] += est_obj.pjugados
            
            # Una vez sumados todos los jugadores de ESTE equipo, vemos si hay un récord
            for jug_obj, total_p in conteo_jugadores_equipo.items():
                if total_p > max_partidos:
                    max_partidos = total_p
                    mejor_jugador = jug_obj
                    mejor_equipo_nombre = equipo_obj.nombre

        return mejor_jugador, (mejor_equipo_nombre, int(max_partidos))

    def obtener_jugador_mas_minutos_total(self):
        """
        Suma todos los minutos de todas las temporadas de cada jugador
        para encontrar al que más tiempo ha estado sobre el césped.
        
        Devuelve: (Objeto Jugador, total_minutos)
        """
        max_minutos = -1
        mejor_jugador = None

        for jugador in self.jugadores.values():
            # Sumamos el atributo .minutos de cada objeto Estadistica del jugador
            total_minutos_jugador = sum(est.minutos for est in jugador.estadisticas)
            
            if total_minutos_jugador > max_minutos:
                max_minutos = total_minutos_jugador
                mejor_jugador = jugador

        return mejor_jugador, int(max_minutos)
    
    def obtener_objetos_equipo_jugador(self, nombre_jugador: str):
        """
        Busca a un jugador por su nombre y devuelve la lista de objetos Equipo
        en los que ha militado a lo largo de su carrera.
        
        Devuelve: list[Equipo] o None si el jugador no existe.
        """
        if nombre_jugador in self.jugadores:
            jugador_obj = self.jugadores[nombre_jugador]
            equipos_encontrados = []
            nombres_vistos = set() # Para no repetir el mismo objeto Equipo
            
            for est in jugador_obj.estadisticas:
                nombre_equipo = est.equipo
                
                # Si el equipo está en nuestro diccionario de liga y no lo hemos añadido ya
                if nombre_equipo in self.equipos and nombre_equipo not in nombres_vistos:
                    obj_equipo = self.equipos[nombre_equipo]
                    equipos_encontrados.append(obj_equipo)
                    nombres_vistos.add(nombre_equipo)
            
            return equipos_encontrados
            
        return None
    
    def obtener_top_jugadores_fieles(self, n: int):
        """
        Busca los N jugadores que más temporadas han pasado en un mismo club.
        
        Devuelve: Lista de tuplas [(Objeto Jugador, Objeto Equipo, int temporadas)]
        Orden: 1º Mayor número temporadas, 2º Orden alfabético (A-Z)
        """
        todos_los_registros = []

        # 1. Recorremos cada equipo
        for equipo_obj in self.equipos.values():
            
            # 2. Contamos cuántas temporadas tiene cada jugador en ESTE equipo
            # Usamos un diccionario temporal {Jugador: contador}
            conteo_jugador = {}
            for lista_registros in equipo_obj.temporadas.values():
                for jug_obj, est_obj in lista_registros:
                    conteo_jugador[jug_obj] = conteo_jugador.get(jug_obj, 0) + 1
            
            # 3. Guardamos los resultados de este equipo en nuestra lista maestra
            for jug_obj, num_temps in conteo_jugador.items():
                todos_los_registros.append((jug_obj, equipo_obj, num_temps))

        # 4. ORDENACIÓN MÁGICA:
        # Usamos un signo '-' en x[2] para que las temporadas sean DESCENDENTES
        # Dejamos x[0].nombre normal para que el nombre sea ASCENDENTE (A-Z)
        todos_los_registros.sort(key=lambda x: (-x[2], x[0].nombre))

        # 5. Devolvemos solo los N primeros
        return todos_los_registros[:n]

    

    def obtener_parejas_mas_minutos_juntos(self, n: int):
        """
        Calcula qué parejas de jugadores han acumulado más minutos compartiendo vestuario.
        Suma los minutos de ambos en las temporadas que coincidieron en el mismo club.
        """
        # Diccionario clave: (id_jugador1, id_jugador2, nombre_equipo) -> valor: minutos_totales
        # Usamos los objetos jugador ordenados por nombre para que la pareja siempre sea la misma
        registro_parejas = {}

        for equipo_obj in self.equipos.values():
            # Para cada equipo, miramos temporada a temporada
            for temporada, lista_jugadores in equipo_obj.temporadas.items():
                
                # Generamos todas las combinaciones posibles de 2 jugadores en esta temporada
                # combinations([A, B, C], 2) -> (A,B), (A,C), (B,C)
                for (jug1, est1), (jug2, est2) in combinations(lista_jugadores, 2):
                    
                    # Ordenamos la pareja por nombre para evitar duplicados (A-B es lo mismo que B-A)
                    pareja = tuple(sorted([jug1, jug2], key=lambda x: x.nombre))
                    
                    # La clave incluye el equipo para separar records si jugaron juntos en varios clubes
                    clave = (pareja[0], pareja[1], equipo_obj)
                    
                    minutos_temporada = est1.minutos + est2.minutos
                    
                    if clave not in registro_parejas:
                        registro_parejas[clave] = 0
                    registro_parejas[clave] += minutos_temporada

        # Convertimos a lista para ordenar
        resultado = []
        for (j1, j2, eq), minutos in registro_parejas.items():
            resultado.append((j1, j2, eq, int(minutos)))

        # Ordenamos por minutos descendente
        resultado.sort(key=lambda x: x[3], reverse=True)

        return resultado[:n]
    
    def obtener_jugadores_menos_lesiones_mas_partidos(self, n: int):
        ranking = []

        for jugador in self.jugadores.values():
            # Sumamos totales de este jugador
            t_jugados = sum(est.pjugados for est in jugador.estadisticas)
            t_lesiones = sum(est.lesiones for est in jugador.estadisticas) 
            
            # Solo metemos a los que hayan jugado algo
            if t_jugados > 0:
                ranking.append((jugador, int(t_lesiones), int(t_jugados)))

        # LA CLAVE DE LA ORDENACIÓN MÚLTIPLE:
        # x[1] son las lesiones (de menos a más)
        # -x[2] son los partidos jugados (el menos indica de más a menos)
        ranking.sort(key=lambda x: (x[1], -x[2]))

        return ranking[:n]


