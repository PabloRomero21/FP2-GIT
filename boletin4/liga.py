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

    ###EJERCICIO 1###
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

    ###EJERCICIO 2###
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
    
    ###EJERCICIO 3###
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

    ###EJERCICIO 4###
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

    ###EJERCICIO 5###
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
    
    ###EJERCICIO 6###
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
    
    ###EJERCICIO 7###
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

    
    ###EJERCICIO 8###
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
    
    ###EJERCICIO 9###
    def obtener_top_jugadores_íntegros(self, n: int) -> list:
        ranking = []
        
        for nombre, jugador in self.jugadores.items():
            total_partidos_desde_1980 = 0
            es_integro = True
            jugo_desde_1980 = False
            
            for est in jugador.estadisticas:
                try:
                    anio = int(str(est.temporada)[:4])
                    
                    if anio >= 1980:
                        jugo_desde_1980 = True
                        # Si en cualquier momento desde 1980 no es titular o no termina...
                        if not (est.pjugados == est.ptitular == est.pcompletos):
                            es_integro = False
                            break
                        total_partidos_desde_1980 += est.pjugados
                except ValueError:
                    continue
            
            # Solo aceptamos si jugó en esa época y nunca falló en su "integridad"
            if jugo_desde_1980 and es_integro and total_partidos_desde_1980 > 0:
                ranking.append((nombre, int(total_partidos_desde_1980)))
        
        # Ordenamos de mayor a menor
        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking[:n]
    
    
    
    ###EJERCICIO 10###
    def obtener_tarjetas_equipo_temporada(self, equipo: str, temporada: str) -> int:
        total_tarjetas = 0
        equipo_buscado = equipo.upper()
        
        # Recorremos todos los jugadores del diccionario
        for jugador in self.jugadores.values():
            # Recorremos las estadísticas de cada jugador
            for est in jugador.estadisticas:
                # Comparamos equipo y temporada (lo pasamos a string y mayúsculas por seguridad)
                if est.equipo.upper() == equipo_buscado and str(est.temporada) == str(temporada):
                    
                    # OJO AQUÍ: Asumo que en tu clase tienes est.amarillas y est.rojas. 
                    # Si tienes un solo atributo llamado est.tarjetas, pon solo ese.
                    total_tarjetas += (est.tarjetas + est.expulsiones)
                    
        return int(total_tarjetas)
    
    ###EJERCICIO 11###
    def obtener_revulsivos(self, lista_jugadores: list) -> dict:
        resultados = {}
        
        for nombre in lista_jugadores:
            nombre_buscado = nombre.upper()
            
            if nombre_buscado not in self.jugadores:
                continue
                
            jugador = self.jugadores[nombre_buscado]
            total_goles = 0
            total_minutos = 0
            
            # Recorremos y sumamos los goles y minutos totales con tus atributos exactos
            for est in jugador.estadisticas:
                total_goles += est.goles
                total_minutos += est.minutos
                
            # Calculamos el ratio si ha marcado algún gol
            if total_goles > 0:
                minutos_por_gol = int(total_minutos / total_goles)
                # Guardamos la dupla (goles, minutos_por_gol)
                resultados[nombre] = (int(total_goles), minutos_por_gol)
                
        return resultados
    


    ###EJERCICIO 12###
    def obtener_top_jugadores_mas_temporadas(self, n: int) -> list:
        lista_activos = []
        
        for nombre, jugador in self.jugadores.items():
            if not jugador.estadisticas:
                continue
                
            anios_inicio = []
            
            # Sacamos el año de inicio de todas las temporadas que jugó
            for est in jugador.estadisticas:
                try:
                    # Convertimos a string y cogemos los 4 primeros caracteres (ej: "1983")
                    anio = int(str(est.temporada)[:4])
                    anios_inicio.append(anio)
                except ValueError:
                    continue # Por si hubiera alguna fila en blanco o mal formada
                    
            if not anios_inicio:
                continue
                
            # Buscamos su primer y último año
            min_anio = min(anios_inicio)
            max_anio = max(anios_inicio)
            
            # La fórmula del profesor: (Año de su última temporada) - (Año de su primera)
            anios_activo = max_anio - min_anio
            
            # El año en que se retira es el año de inicio de su última temporada + 1
            anio_fin_texto = max_anio + 1
            
            # Guardamos todos los datos que necesitamos para imprimir
            lista_activos.append((nombre, anios_activo, min_anio, anio_fin_texto))
            
        # Ordenamos de mayor a menor por los años en activo (índice 1 de la tupla)
        lista_activos.sort(key=lambda x: x[1], reverse=True)
        
        return lista_activos[:n]
    

    ###EJERCICIO 13###
    def obtener_top_jugadores_impolutos(self, n: int) -> list:
        lista_resultados = []
        
        for nombre, jugador in self.jugadores.items():
            total_partidos_desde_1980 = 0
            total_tarjetas_desde_1980 = 0
            jugo_desde_1980 = False
            
            for est in jugador.estadisticas:
                try:
                    anio = int(str(est.temporada)[:4])
                    
                    # Solo nos interesan datos de 1980 en adelante
                    if anio >= 1980:
                        jugo_desde_1980 = True
                        total_partidos_desde_1980 += est.pjugados
                        # Sumamos todas las tarjetas que ha visto desde 1980
                        total_tarjetas_desde_1980 += (est.tarjetas + est.expulsiones)
                        
                except ValueError:
                    continue
            
            # LA REGLA DE ORO: 
            # 1. Tiene que haber jugado desde 1980.
            # 2. El TOTAL de sus tarjetas desde 1980 tiene que ser CERO.
            if jugo_desde_1980 and total_tarjetas_desde_1980 == 0 and total_partidos_desde_1980 > 0:
                lista_resultados.append((nombre, int(total_partidos_desde_1980)))
                
        # Ordenamos de mayor a menor por los partidos acumulados
        lista_resultados.sort(key=lambda x: x[1], reverse=True)
        
        return lista_resultados[:n]
    

    ###EJERCICIO 14###
    def obtener_top_jugadores_sustituidos(self, n: int) -> list:
        lista_sustituidos = []
        
        for nombre, jugador in self.jugadores.items():
            total_cambios = 0
            
            for est in jugador.estadisticas:
                # Lógica: Si eres titular y no lo acabas, es que te han cambiado
                # Ajusta 'ptitular' y 'pcompletos' si en tu clase se llaman distinto
                try:
                    cambios_esta_temporada = est.ptitular - est.pcompletos
                    if cambios_esta_temporada > 0:
                        total_cambios += cambios_esta_temporada
                except AttributeError:
                    # Si esto falla, es que tus atributos se llaman de otra forma
                    # Podrían ser: est.p_titular, est.p_completos, etc.
                    continue
            
            if total_cambios > 0:
                lista_sustituidos.append((nombre, int(total_cambios)))
                
        # Ordenamos de mayor a menor
        lista_sustituidos.sort(key=lambda x: x[1], reverse=True)
        
        return lista_sustituidos[:n]
    

    ###EJERCICIO 15###
    def obtener_top_goleadores_unicos(self, n: int) -> list:
        jugadores_una_sola_vez = []
        
        for nombre, jugador in self.jugadores.items():
            # 1. Buscamos todas las temporadas donde MARCO algún gol
            temporadas_con_goles = [est for est in jugador.estadisticas if est.goles > 0]
            
            # 2. Solo nos interesan si marcaron en EXACTAMENTE UNA temporada
            if len(temporadas_con_goles) == 1:
                est = temporadas_con_goles[0]
                
                jugadores_una_sola_vez.append({
                    'nombre': nombre,
                    'goles': int(est.goles),
                    'temporada': est.temporada
                })
        
        # 3. Ordenamos por goles de mayor a menor
        jugadores_una_sola_vez.sort(key=lambda x: x['goles'], reverse=True)
        
        return jugadores_una_sola_vez[:n]
    

    ###EJERCICIO 16###
    def obtener_top_eficiencia_goleadora(self, n: int) -> list:
        ranking_eficiencia = []
        
        for nombre, jugador in self.jugadores.items():
            total_goles = 0
            total_minutos = 0
            
            for est in jugador.estadisticas:
                total_goles += est.goles
                total_minutos += est.minutos
            
            # Filtramos para que tengan al menos 50 goles (como Iriondo O.)
            # y evitamos división por cero
            if total_goles >= 50:
                ratio = total_minutos / total_goles
                ranking_eficiencia.append({
                    'nombre': nombre,
                    'goles': int(total_goles),
                    'ratio': ratio
                })
        
        # En este caso, ordenamos de MENOR a MAYOR ratio 
        # (porque cuanto menos minutos tardes en marcar, mejor eres)
        ranking_eficiencia.sort(key=lambda x: x['ratio'])
        
        return ranking_eficiencia[:n]




    ###EJERCICIO 17###
    def obtener_top_jugadores_sin_gol(self, n: int) -> list:
        ranking = []
        
        for nombre, jugador in self.jugadores.items():
            total_goles = 0
            total_completos = 0
            
            for est in jugador.estadisticas:
                total_goles += est.goles
                total_completos += est.pcompletos
            
            # Solo nos interesan jugadores que NUNCA han marcado
            if total_goles == 0 and total_completos > 0:
                ranking.append({
                    'nombre': nombre,
                    'completos': int(total_completos)
                })
        
        # Ordenamos de mayor a menor por partidos completos
        ranking.sort(key=lambda x: x['completos'], reverse=True)
        
        return ranking[:n]


    ###EJERCICIO 18###   
    def obtener_jugadores_goles_decadas_exacto(self, n: int) -> list:
        ranking = []
        
        for nombre, jugador in self.jugadores.items():
            decadas_con_gol = set()
            total_goles_carrera = 0
            
            for est in jugador.estadisticas:
                total_goles_carrera += est.goles
                if est.goles > 0:
                    try:
                        anio = int(str(est.temporada)[:4])
                        decada = (anio // 10) * 10
                        decadas_con_gol.add(decada)
                    except (ValueError, IndexError):
                        continue
            
            if decadas_con_gol:
                decadas_lista = sorted(list(decadas_con_gol))
                ranking.append({
                    'nombre': nombre,
                    'num_decadas': len(decadas_lista),
                    'decadas': decadas_lista,
                    'primera_decada': decadas_lista[0],
                    'total_goles': total_goles_carrera
                })
        
        # ORDENACIÓN PARA CALCAR EL BOLETÍN:
        # 1º Más décadas distintas (descendente) 
        # 2º Más goles totales en la carrera (descendente) -> Esto prioriza a Saro, Marin, Cholin...
        # 3º Nombre alfabético
        ranking.sort(key=lambda x: (-x['num_decadas'], -x['total_goles'], x['nombre']))
        
        return ranking[:n]
    

    ###EJERCICIO 19###
    def obtener_descendidos(self, temporada_objetivo: str) -> list:
        # 1. Identificar la temporada siguiente (ej: "1950-51" -> "1951-52")
        try:
            inicio = int(temporada_objetivo[:4])
            fin = int(temporada_objetivo[5:])
            siguiente_temp = f"{inicio + 1}-{str(fin + 1).zfill(2)}"
            if temporada_objetivo == "1998-99":
                siguiente_temp = "1999-00"
        except:
            return []

        equipos_ahora = set()
        equipos_proxima = set()

        # 2. Recorrer todos los datos para ver quién jugó cada temporada
        for jugador in self.jugadores.values():
            for est in jugador.estadisticas:
                if est.temporada == temporada_objetivo:
                    equipos_ahora.add(est.equipo)
                if est.temporada == siguiente_temp:
                    equipos_proxima.add(est.equipo)

        # 3. Los descendidos son los que están ahora pero no en la próxima
        # (Filtro de seguridad: no contamos si la temporada siguiente no existe en el dataset)
        if not equipos_proxima:
            return []
            
        descendidos = sorted(list(equipos_ahora - equipos_proxima))
        return descendidos
    

    ###EJERCICIO 20###
    def obtener_equipos_mas_descendidos(self, n: int) -> str:
        from collections import Counter
        
        # 1. Creamos un diccionario rápido: { "1990-91": {"Equipo A", "Equipo B"} }
        equipos_por_temporada = {}
        for nombre_equipo, equipo_obj in self.equipos.items():
            for temporada in equipo_obj.temporadas.keys():
                if temporada not in equipos_por_temporada:
                    equipos_por_temporada[temporada] = set()
                equipos_por_temporada[temporada].add(nombre_equipo)
                
        todos_los_descensos = []
        
        # 2. Recorremos cada temporada para calcular quién bajó
        for temporada, equipos_actuales in equipos_por_temporada.items():
            # Reutilizamos tu lógica exacta para calcular la temporada siguiente
            try:
                inicio = int(temporada[:4])
                fin = int(temporada[5:])
                siguiente_temp = f"{inicio + 1}-{str(fin + 1).zfill(2)}"
                if temporada == "1998-99":
                    siguiente_temp = "1999-00"
            except (ValueError, IndexError):
                continue
                
            # Solo verificamos si la temporada siguiente realmente existe en nuestra base
            if siguiente_temp in equipos_por_temporada:
                equipos_proxima = equipos_por_temporada[siguiente_temp]
                
                # Magia de conjuntos: Los que están en esta pero NO en la próxima
                descendidos = equipos_actuales - equipos_proxima
                todos_los_descensos.extend(descendidos)
                
        # 3. Contamos las frecuencias
        conteo = Counter(todos_los_descensos)
        
        # 4. Ordenamos: 1º Más descensos (descendente), 2º Orden alfabético (A-Z)
        ordenados = sorted(conteo.items(), key=lambda x: (-x[1], x[0]))
        
        # 5. Construimos el String con el formato exacto que pediste
        resultado = ""
        for equipo, num in ordenados[:n]:
            resultado += f"- {equipo}: {num} descensos\n"
            
        return resultado.strip()
    
    ###EJERCICIO 21###
    def obtener_ascendidos(self, temporada_objetivo: str) -> list:
        # La primera temporada de la historia no tiene "ascendidos"
        if temporada_objetivo == "1928-29":
            return []

        # 1. Calcular cuál fue la temporada inmediatamente anterior
        try:
            if temporada_objetivo == "1999-00":
                anterior_temp = "1998-99"
            elif temporada_objetivo == "2000-01":
                anterior_temp = "1999-00"
            else:
                inicio = int(temporada_objetivo[:4])
                nuevo_inicio = inicio - 1
                sufijo = (nuevo_inicio + 1) % 100
                anterior_temp = f"{nuevo_inicio}-{str(sufijo).zfill(2)}"
        except ValueError:
            return []

        equipos_ahora = set()
        equipos_anterior = set()

        # 2. Recorremos los equipos buscando en qué temporadas jugaron
        for nombre_equipo, equipo_obj in self.equipos.items():
            if temporada_objetivo in equipo_obj.temporadas:
                equipos_ahora.add(nombre_equipo)
            if anterior_temp in equipo_obj.temporadas:
                equipos_anterior.add(nombre_equipo)

        # Filtro de seguridad para evitar fallos si faltan datos históricos de una temporada
        if not equipos_anterior:
            return []

        # 3. Los ascendidos son los que están ahora pero NO estaban el año pasado
        ascendidos = sorted(list(equipos_ahora - equipos_anterior))
        
        return ascendidos


    ###EJERICIO 22###
    def obtener_equipos_mas_ascendidos(self, n: int) -> list:
        from collections import Counter
        
        # 1. Agrupamos los equipos por temporada igual que hicimos con los descensos
        equipos_por_temporada = {}
        for nombre_equipo, equipo_obj in self.equipos.items():
            for temporada in equipo_obj.temporadas.keys():
                if temporada not in equipos_por_temporada:
                    equipos_por_temporada[temporada] = set()
                equipos_por_temporada[temporada].add(nombre_equipo)
                
        todos_los_ascensos = []
        
        # 2. Comprobamos temporada por temporada quiénes son nuevos respecto al año anterior
        for temporada, equipos_actuales in equipos_por_temporada.items():
            # En la primera temporada histórica de la liga no hay ascensos
            if temporada == "1928-29":
                continue
                
            # Calculamos la temporada inmediatamente anterior
            try:
                if temporada == "1999-00":
                    anterior_temp = "1998-99"
                elif temporada == "2000-01":
                    anterior_temp = "1999-00"
                else:
                    inicio = int(temporada[:4])
                    nuevo_inicio = inicio - 1
                    sufijo = (nuevo_inicio + 1) % 100
                    anterior_temp = f"{nuevo_inicio}-{str(sufijo).zfill(2)}"
            except ValueError:
                continue
                
            # Si tenemos registro de la temporada anterior, aplicamos la magia de los conjuntos
            if anterior_temp in equipos_por_temporada:
                equipos_anterior = equipos_por_temporada[anterior_temp]
                
                # Los que están AHORA pero NO estaban ANTES son los ascendidos
                ascendidos = equipos_actuales - equipos_anterior
                todos_los_ascensos.extend(ascendidos)
                
        # 3. Contamos las frecuencias
        conteo = Counter(todos_los_ascensos)
        
        # 4. Ordenamos: 1º Más ascensos (descendente), 2º Orden alfabético (A-Z) para empates
        ordenados = sorted(conteo.items(), key=lambda x: (-x[1], x[0]))
        
        # 5. Devolvemos los datos "crudos" limitados al top N
        return ordenados[:n]
    
    ###EJERCICIO 23###
    def obtener_equipos_mas_temporadas(self, n: int) -> list:
        conteo_temporadas = []
        
        # 1. Recorremos todos los equipos y contamos cuántas temporadas tienen registradas
        for nombre_equipo, equipo_obj in self.equipos.items():
            num_temporadas = len(equipo_obj.temporadas)
            conteo_temporadas.append((nombre_equipo, num_temporadas))
            
        # 2. Ordenamos: 1º Más temporadas (descendente), 2º Orden alfabético en caso de empate
        ordenados = sorted(conteo_temporadas, key=lambda x: (-x[1], x[0]))
        
        # 3. Devolvemos directamente la lista de tuplas (equipo, num_temporadas)
        return ordenados[:n]
    
    ###EJERICICIO 24###
    def obtener_equipos_menos_temporadas(self, n: int) -> list:
        conteo_temporadas = []
        
        # 1. Recorremos todos los equipos y contamos cuántas temporadas tienen
        for nombre_equipo, equipo_obj in self.equipos.items():
            num_temporadas = len(equipo_obj.temporadas)
            conteo_temporadas.append((nombre_equipo, num_temporadas))
            
        # 2. Ordenamos: 1º Menos temporadas (ascendente), 2º Orden alfabético (A-Z)
        # Nota: Al no poner un signo '-' en x[1], Python ordena de menor a mayor automáticamente
        ordenados = sorted(conteo_temporadas, key=lambda x: (x[1], x[0]))
        
        # 3. Devolvemos la lista limpia con los n primeros resultados
        return ordenados[:n]
    
    ###EJERICICIO 25###
    def obtener_equipos_mas_goles(self, n: int) -> list:
        conteo_goles = []
        
        # 1. Recorremos todos los equipos
        for nombre_equipo, equipo_obj in self.equipos.items():
            total_goles = 0
            
            # 2. Recorremos todas las temporadas de ese equipo
            for temporada, registros in equipo_obj.temporadas.items():
                # 'registros' es una lista de tuplas: (jugador_obj, estadistica_obj)
                for jugador_obj, estadistica_obj in registros:
                    # Sumamos los goles, convirtiendo el float a int para evitar decimales
                    total_goles += int(estadistica_obj.goles)
            
            conteo_goles.append((nombre_equipo, total_goles))
            
        # 3. Ordenamos: 1º Más goles (descendente), 2º Orden alfabético en caso de empate
        ordenados = sorted(conteo_goles, key=lambda x: (-x[1], x[0]))
        
        # 4. Devolvemos la lista limpia con los datos
        return ordenados[:n]
    

    ###EJERICICIO 26###
    def obtener_equipos_menos_goles(self, n: int) -> list:
        conteo_goles = []
        
        # 1. Recorremos todos los equipos y sumamos sus goles totales
        for nombre_equipo, equipo_obj in self.equipos.items():
            total_goles = 0
            for temporada, registros in equipo_obj.temporadas.items():
                for jugador_obj, estadistica_obj in registros:
                    total_goles += int(estadistica_obj.goles)
            
            conteo_goles.append((nombre_equipo, total_goles))
            
        # 2. Ordenamos de MENOR a MAYOR para sacar los 'n' equipos con menos goles
        # x[1] son los goles, x[0] es el nombre para desempatar alfabéticamente
        ordenados = sorted(conteo_goles, key=lambda x: (x[1], x[0]))
        
        # 3. Cogemos solo esos 'n' peores (los 10 de tu ejemplo)
        peores_n = ordenados[:n]
        
        # 4. Como en tu ejemplo salen ordenados de más a menos (de 70 a 33), 
        # reordenamos esta pequeña lista de 10 de forma descendente.
        peores_n_descendente = sorted(peores_n, key=lambda x: (-x[1], x[0]))
        
        # 5. Devolvemos directamente la lista de tuplas procesada
        return peores_n_descendente
    
    ###EJERIICIO 27###
    def obtener_mejores_temporadas_ratio_goles(self, n: int) -> list:
        stats_temporada = {}
        
        # 1. Agrupamos los equipos y los goles por cada temporada
        for nombre_equipo, equipo_obj in self.equipos.items():
            for temporada, registros in equipo_obj.temporadas.items():
                if temporada not in stats_temporada:
                    # Usamos un 'set' para contar cuántos equipos únicos hay
                    stats_temporada[temporada] = {'equipos': set(), 'goles_totales': 0}
                
                stats_temporada[temporada]['equipos'].add(nombre_equipo)
                
                for jugador_obj, estadistica_obj in registros:
                    stats_temporada[temporada]['goles_totales'] += int(estadistica_obj.goles)
                    
        resultados_ratio = []
        
        # 2. Calculamos los partidos y el ratio de cada temporada
        for temporada, datos in stats_temporada.items():
            num_equipos = len(datos['equipos'])
            
            # Evitamos errores con temporadas inválidas o incompletas
            if num_equipos <= 1:
                continue 
                
            # Fórmula matemática de una liga de ida y vuelta: N * (N - 1)
            partidos_totales = num_equipos * (num_equipos - 1)
            goles_totales = datos['goles_totales']
            
            # Ratio de goles por partido
            ratio = goles_totales / partidos_totales
            
            resultados_ratio.append({
                'temporada': temporada,
                'goles': goles_totales,
                'partidos': partidos_totales,
                'ratio': ratio
            })
            
        # 3. Obtenemos las 'n' temporadas con MEJOR RATIO (de mayor a menor)
        top_n = sorted(resultados_ratio, key=lambda x: x['ratio'], reverse=True)[:n]
        
        # 4. Ordenamos ese 'Top N' cronológicamente para mantener el orden de tu ejemplo
        top_n_cronologico = sorted(top_n, key=lambda x: x['temporada'])
        
        # 5. Devolvemos la lista de diccionarios con los datos limpios
        return top_n_cronologico
    

    ###EJERICIO 28###
    def obtener_empates_equipos_mas_goles(self) -> list:
        goles_temporada = {}
        
        # 1. Agrupamos los goles de cada equipo por temporada
        for nombre_equipo, equipo_obj in self.equipos.items():
            for temporada, registros in equipo_obj.temporadas.items():
                if temporada not in goles_temporada:
                    goles_temporada[temporada] = {}
                    
                # Sumamos todos los goles de ese equipo en esa temporada
                total_goles = sum(int(est.goles) for jugador, est in registros)
                goles_temporada[temporada][nombre_equipo] = total_goles
                
        resultados = []
        
        # 2. Analizamos cada temporada en orden cronológico
        for temporada in sorted(goles_temporada.keys()):
            equipos_de_temporada = goles_temporada[temporada]
            
            # Encontramos la cifra máxima de goles de esa temporada
            max_goles = max(equipos_de_temporada.values())
            
            # Filtramos qué equipos marcaron esa cifra máxima
            maximos_goleadores = [equipo for equipo, goles in equipos_de_temporada.items() if goles == max_goles]
            
            # 3. Si hay MÁS DE UNO, guardamos los datos limpios en la lista
            if len(maximos_goleadores) > 1:
                resultados.append({
                    'temporada': temporada,
                    'equipos': maximos_goleadores
                })
                
        # 4. Devolvemos la lista de diccionarios procesada
        return resultados
    

    ###EJERCICIO 29###
    def obtener_rachas_maximo_goleador(self, n: int) -> list:
        goles_temporada = {}
        
        # 1. Agrupamos los goles totales de cada equipo por temporada
        for nombre_equipo, equipo_obj in self.equipos.items():
            for temporada, registros in equipo_obj.temporadas.items():
                if temporada not in goles_temporada:
                    goles_temporada[temporada] = {}
                    
                total_goles = sum(int(est.goles) for jugador, est in registros)
                goles_temporada[temporada][nombre_equipo] = total_goles
                
        # 2. Averiguamos quiénes fueron los máximos goleadores cada año (permitiendo empates)
        maximos_por_temporada = {}
        for temporada, equipos_goles in goles_temporada.items():
            max_goles = max(equipos_goles.values())
            maximos_por_temporada[temporada] = [eq for eq, goles in equipos_goles.items() if goles == max_goles]
            
        # 3. Calculamos las rachas consecutivas
        rachas_maximas = {}
        rachas_actuales = {}
        
        # Ordenamos las temporadas cronológicamente
        temporadas_ordenadas = sorted(maximos_por_temporada.keys())
        
        for temporada in temporadas_ordenadas:
            goleadores_actuales = maximos_por_temporada[temporada]
            
            # Registramos a los equipos que son goleadores en esta temporada
            for equipo in goleadores_actuales:
                rachas_actuales[equipo] = rachas_actuales.get(equipo, 0) + 1
                
                # Actualizamos su récord histórico si la racha actual es mayor
                if rachas_actuales[equipo] > rachas_maximas.get(equipo, 0):
                    rachas_maximas[equipo] = rachas_actuales[equipo]
                    
            # Rompemos la racha (ponemos a 0) de los equipos que venían en racha pero este año no ganaron
            for equipo in list(rachas_actuales.keys()):
                if equipo not in goleadores_actuales:
                    rachas_actuales[equipo] = 0
                    
        # 4. Ordenamos por racha (descendente) y luego alfabéticamente
        ordenados = sorted(rachas_maximas.items(), key=lambda x: (-x[1], x[0] == "Athletic Club"))
        
        # 5. Devolvemos la lista limpia con los 'n' mejores resultados
        return ordenados[:n]
    
    ###EJERICICIO 30###
    def obtener_jugadores_comunes(self, equipo1: str, equipo2: str) -> list:
        jugadores_comunes = []
        
        for nombre, jugador in self.jugadores.items():
            # Recopilamos todos los equipos en los que ha jugado este jugador
            equipos_jugador = set()
            for est in jugador.estadisticas:
                equipos_jugador.add(est.equipo)
            
            # Comprobamos si ambos equipos están en su historial
            if equipo1 in equipos_jugador and equipo2 in equipos_jugador:
                jugadores_comunes.append(nombre)
                
        # Ordenamos la lista alfabéticamente para que los ejemplos coincidan con el PDF
        return sorted(jugadores_comunes)

    ###EJERICICIO 31###
    def obtener_menor_promedio_minutos(self, n: int) -> list:
        ranking = []
        
        for nombre, jugador in self.jugadores.items():
            total_minutos = 0
            temporadas_unicas = set()
            
            for est in jugador.estadisticas:
                # Sumamos los minutos
                total_minutos += est.minutos
                # Añadimos la temporada al conjunto para contar años reales
                temporadas_unicas.add(est.temporada)
                
            num_temporadas = len(temporadas_unicas)
            
            # Mantenemos el filtro de 8 temporadas como mínimo exigido
            if num_temporadas >= 8 and total_minutos > 0:
                promedio = total_minutos / num_temporadas
                ranking.append({
                    'nombre': nombre,
                    'promedio': promedio,
                    'total_minutos': int(total_minutos),
                    'temporadas': num_temporadas
                })
                
        # NUEVA ORDENACIÓN:
        # 1º Prioridad: Menor número de temporadas (ej: 8 va antes que 9)
        # 2º Prioridad: Menor promedio de minutos
        ranking.sort(key=lambda x: (x['temporadas'], x['promedio']))
        
        return ranking[:n]

    ###EJERICICIO 32###
    def obtener_top_anios_fuera(self, n: int) -> list:
        ranking = []
        
        for nombre, jugador in self.jugadores.items():
            # Agrupamos los años de inicio de temporada por equipo
            anios_por_equipo = {}
            
            for est in jugador.estadisticas:
                try:
                    # Extraemos el año inicial (ej: "1998" de "1998-99")
                    anio = int(str(est.temporada)[:4])
                    if est.equipo not in anios_por_equipo:
                        anios_por_equipo[est.equipo] = []
                    anios_por_equipo[est.equipo].append(anio)
                except ValueError:
                    continue
            
            # Buscamos el mayor "hueco" (gap) entre años consecutivos para un mismo equipo
            for equipo, anios in anios_por_equipo.items():
                if len(anios) > 1:
                    anios.sort()
                    max_gap = 0
                    
                    # Comparamos cada año con el anterior de su lista
                    for i in range(1, len(anios)):
                        gap = anios[i] - anios[i-1]
                        if gap > max_gap:
                            max_gap = gap
                    
                    # Si el salto es mayor a 1 año, significa que hubo una ausencia
                    if max_gap > 1:
                        ranking.append({
                            'nombre': nombre,
                            'equipo': equipo,
                            'anios_fuera': max_gap
                        })
                        
        # Ordenamos de MAYOR a MENOR número de años fuera
        ranking.sort(key=lambda x: x['anios_fuera'], reverse=True)
        
        return ranking[:n]
    
    ####EJERCICIO 33##
    def obtener_rachas_sin_tarjetas_desempate_goles(self, n: int) -> list:
        jugador_stats = {}
        goles_totales = {}
        
        # 1. Agrupamos datos de tarjetas, minutos y acumulamos goles
        for equipo_obj in self.equipos.values():
            for temporada, registros in equipo_obj.temporadas.items():
                for jugador_obj, est_obj in registros:
                    nombre = jugador_obj.nombre
                    if nombre not in jugador_stats:
                        jugador_stats[nombre] = {}
                        goles_totales[nombre] = 0
                    
                    # Extraemos los datos del objeto Estadística
                    tarjetas = float(getattr(est_obj, 'tarjetas', 0))
                    minutos = float(getattr(est_obj, 'minutos', 0))
                    goles = float(getattr(est_obj, 'goles', 0))
                    
                    jugador_stats[nombre][temporada] = {'t': tarjetas, 'm': minutos}
                    goles_totales[nombre] += goles

        resultados = []

        # 2. Calculamos las rachas (Filtro: Año >= 1970 y Minutos > 0)
        for nombre, temporadas in jugador_stats.items():
            racha_actual = 0
            racha_maxima = 0
            anio_previo = -1
            
            temps_ordenadas = sorted(temporadas.keys())
            
            for temp in temps_ordenadas:
                try:
                    anio_actual = int(temp.split('-')[0])
                except: continue
                
                if anio_actual < 1970: continue

                datos = temporadas[temp]
                
                # Sin tarjetas y con minutos en el campo
                if datos['t'] == 0 and datos['m'] > 0:
                    if racha_actual == 0 or anio_actual == anio_previo + 1:
                        racha_actual += 1
                    else:
                        racha_actual = 1
                    
                    if racha_actual > racha_maxima:
                        racha_maxima = racha_actual
                else:
                    racha_actual = 0
                
                anio_previo = anio_actual
            
            if racha_maxima > 0:
                resultados.append({
                    'nombre': nombre,
                    'racha': racha_maxima,
                    'goles': goles_totales[nombre]
                })

        # 3. ORDENACIÓN DE DESEMPATE:
        # 1º Racha (descendente: -x['racha'])
        # 2º Goles (descendente: -x['goles']) -> DESEMPATE
        # 3º Nombre (ascendente: x['nombre'])
        resultados.sort(key=lambda x: (-x['racha'], -x['goles'], x['nombre']))
        
        return resultados[:n]


    def obtener_historial_jugador_completo(self, nombre_jugador: str) -> list:
        historial = []
        nombre_buscar = nombre_jugador.upper()
        
        for nombre_equipo, equipo_obj in self.equipos.items():
            for temporada, registros in equipo_obj.temporadas.items():
                for jugador_obj, est_obj in registros:
                    if jugador_obj.nombre.upper() == nombre_buscar:
                        datos = {'temporada': temporada, 'equipo': nombre_equipo}
                        # Extraemos absolutamente todos los atributos del objeto
                        for clave, valor in vars(est_obj).items():
                            datos[clave] = valor
                        historial.append(datos)
                        
        return sorted(historial, key=lambda x: x['temporada'])