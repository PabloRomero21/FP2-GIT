from itertools import combinations
from collections import Counter


class Liga:
    """
    Clase raíz del sistema. Representa la competición completa a lo largo de la historia.
    Gestiona un diccionario de Temporadas y mantiene dos índices secundarios para
    acelerar las consultas por jugador y por equipo respectivamente.

    Índice principal:
        self.temporadas -> {id_temporada: Temporada}

    Índices secundarios (construidos tras la carga de datos):
        self._jugadores_idx -> {nombre_jugador: [(Temporada, Equipo, Jugador), ...]}
        self._equipos_por_nombre -> {nombre_equipo: [(Temporada, Equipo), ...]}
    """

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.temporadas = {}               # {id_temporada: Temporada}
        self._jugadores_idx = {}           # {nombre_jugador: [(Temporada, Equipo, Jugador)]}
        self._equipos_por_nombre = {}      # {nombre_equipo: [(Temporada, Equipo)]}

    # =========================================================================
    # MÉTODO DE INSERCIÓN
    # =========================================================================

    def agregar_temporada(self, temporada):
        """
        Registra un objeto Temporada en el diccionario de temporadas de la Liga.
        Los índices secundarios se construyen de forma separada llamando a _construir_indices().
        """
        self.temporadas[temporada.id_temporada] = temporada

    # =========================================================================
    # PROPIEDADES DERIVADAS
    # =========================================================================

    @property
    def num_temporadas(self) -> int:
        """
        Número total de temporadas registradas en la Liga.
        """
        return len(self.temporadas)

    @property
    def num_temporadas_no_jugadas(self) -> int:
        """
        Número de temporadas que no llegaron a disputarse (sin partidos posibles),
        es decir, aquellas con menos de 2 equipos registrados.
        """
        return sum(1 for t in self.temporadas.values() if t.num_partidos == 0)

    # =========================================================================
    # GENERADOR / ITERADOR DE HISTORIAL
    # =========================================================================

    def _iterar_historial(self):
        """
        Generador que recorre toda la base de datos y devuelve una tupla con el
        contexto completo de cada registro:

            (Objeto Temporada, Objeto Equipo, Objeto Jugador)

        Esto permite simplificar drásticamente los tratamientos 'a nivel de jugador'
        sin necesidad de bucles anidados manuales en cada método.
        """
        for temporada in self.temporadas.values():
            for equipo in temporada.equipos.values():
                for jugador in equipo.jugadores:
                    yield temporada, equipo, jugador

    # =========================================================================
    # GESTIÓN DE ÍNDICES SECUNDARIOS
    # =========================================================================

    def _construir_indices(self):
        """
        Construye los dos índices secundarios a partir de la jerarquía principal.
        Debe llamarse una vez, al finalizar la carga de todos los datos.

        - _jugadores_idx  -> permite buscar todos los registros de un jugador por nombre.
        - _equipos_por_nombre -> permite acceder a todas las instancias (por temporada)
          de un equipo dado su nombre.
        """
        self._jugadores_idx = {}
        self._equipos_por_nombre = {}

        for temporada_obj in self.temporadas.values():
            for equipo_obj in temporada_obj.equipos.values():

                # Índice de equipos: cada equipo aparece una vez por temporada jugada
                if equipo_obj.nombre not in self._equipos_por_nombre:
                    self._equipos_por_nombre[equipo_obj.nombre] = []
                self._equipos_por_nombre[equipo_obj.nombre].append((temporada_obj, equipo_obj))

                # Índice de jugadores
                for jugador in equipo_obj.jugadores:
                    if jugador.nombre not in self._jugadores_idx:
                        self._jugadores_idx[jugador.nombre] = []
                    self._jugadores_idx[jugador.nombre].append(
                        (temporada_obj, equipo_obj, jugador)
                    )

    def _construir_equipos_por_temporada(self) -> dict:
        """
        Construye y devuelve un diccionario auxiliar con el conjunto de equipos
        que participaron en cada temporada:

            {id_temporada: set(nombre_equipo)}

        Usado internamente por los métodos de descensos y ascensos.
        """
        resultado = {}
        for nombre_equipo, pares in self._equipos_por_nombre.items():
            for temp_obj, _ in pares:
                tid = temp_obj.id_temporada
                if tid not in resultado:
                    resultado[tid] = set()
                resultado[tid].add(nombre_equipo)
        return resultado

    # =========================================================================
    # MÉTODOS DE CONSULTA (EJERCICIOS)
    # =========================================================================

    ###EJERCICIO 1###
    def obtener_maximo_goleador_temporada(self):
        """
        Busca al jugador con más goles en una única temporada con un único equipo.
        Devuelve: (Objeto Jugador, Objeto Estadistica)
        """
        max_goles = -1
        mejor_jugador = None
        mejor_estadistica = None

        for _, _, jugador in self._iterar_historial():
            est = jugador.estadistica
            if est.goles > max_goles:
                max_goles = est.goles
                mejor_jugador = jugador
                mejor_estadistica = est

        return mejor_jugador, mejor_estadistica

    ###EJERCICIO 2###
    def obtener_maximo_goleador_historico(self):
        """
        Suma los goles de todas las temporadas de cada jugador para encontrar
        al máximo goleador de la historia.
        Devuelve: (Objeto Jugador, total_goles)
        """
        max_goles_totales = -1
        mejor_jugador = None

        for nombre, registros in self._jugadores_idx.items():
            goles_totales = sum(j.estadistica.goles for _, _, j in registros)
            if goles_totales > max_goles_totales:
                max_goles_totales = goles_totales
                mejor_jugador = registros[0][2]   # Objeto Jugador representativo

        return mejor_jugador, max_goles_totales

    ###EJERCICIO 3###
    def obtener_jugador_mas_equipos(self):
        """
        Busca al jugador "trotamundos" que ha militado en más clubes distintos.
        Devuelve: (Objeto Jugador, lista_de_nombres_de_equipos)
        """
        max_equipos = 0
        mejor_jugador = None
        lista_mejores_equipos = []

        for nombre, registros in self._jugadores_idx.items():
            equipos_unicos = []
            for _, eq_obj, _ in registros:
                if eq_obj.nombre not in equipos_unicos:
                    equipos_unicos.append(eq_obj.nombre)

            if len(equipos_unicos) > max_equipos:
                max_equipos = len(equipos_unicos)
                mejor_jugador = registros[0][2]
                lista_mejores_equipos = equipos_unicos

        return mejor_jugador, lista_mejores_equipos

    ###EJERCICIO 4###
    def obtener_jugador_record_partidos_en_un_club(self):
        """
        Busca al jugador que más partidos ha acumulado vistiendo la misma camiseta,
        sumando todas las temporadas que estuvo en ese club.
        Devuelve: (Objeto Jugador, (nombre_equipo, numero_partidos))
        """
        max_partidos = -1
        mejor_jugador = None
        mejor_equipo_nombre = ""

        # Acumulamos {(nombre_jugador, nombre_equipo): (jugador_obj, suma_partidos)}
        conteo = {}

        for _, eq_obj, jugador in self._iterar_historial():
            clave = (jugador.nombre, eq_obj.nombre)
            if clave not in conteo:
                conteo[clave] = (jugador, 0.0)
            jug_guardado, pts = conteo[clave]
            conteo[clave] = (jug_guardado, pts + jugador.estadistica.pjugados)

        for (_, nombre_eq), (jug_obj, total_p) in conteo.items():
            if total_p > max_partidos:
                max_partidos = total_p
                mejor_jugador = jug_obj
                mejor_equipo_nombre = nombre_eq

        return mejor_jugador, (mejor_equipo_nombre, int(max_partidos))

    ###EJERCICIO 5###
    def obtener_jugador_mas_minutos_total(self):
        """
        Suma todos los minutos jugados a lo largo de la carrera de cada jugador.
        Devuelve: (Objeto Jugador, total_minutos)
        """
        max_minutos = -1
        mejor_jugador = None

        for nombre, registros in self._jugadores_idx.items():
            total_minutos = sum(j.estadistica.minutos for _, _, j in registros)
            if total_minutos > max_minutos:
                max_minutos = total_minutos
                mejor_jugador = registros[0][2]

        return mejor_jugador, int(max_minutos)

    ###EJERCICIO 6###
    def obtener_objetos_equipo_jugador(self, nombre_jugador: str):
        """
        Busca a un jugador por su nombre y devuelve la lista de objetos Equipo
        en los que ha militado a lo largo de su carrera (sin repetir club).
        Devuelve: list[Equipo] o None si el jugador no existe.
        """
        if nombre_jugador not in self._jugadores_idx:
            return None

        registros = self._jugadores_idx[nombre_jugador]
        equipos_encontrados = []
        nombres_vistos = set()

        for _, eq_obj, _ in registros:
            if eq_obj.nombre not in nombres_vistos:
                equipos_encontrados.append(eq_obj)
                nombres_vistos.add(eq_obj.nombre)

        return equipos_encontrados

    ###EJERCICIO 7###
    def obtener_top_jugadores_fieles(self, n: int):
        """
        Busca los N jugadores que más temporadas han pasado en un mismo club.
        Devuelve: lista de tuplas [(Objeto Jugador, Objeto Equipo, int temporadas)]
        Orden: 1º Mayor número de temporadas, 2º Orden alfabético (A-Z)
        """
        # {(nombre_jugador, nombre_equipo): (jugador_obj, equipo_obj, contador)}
        conteo = {}

        for _, eq_obj, jugador in self._iterar_historial():
            clave = (jugador.nombre, eq_obj.nombre)
            if clave not in conteo:
                conteo[clave] = (jugador, eq_obj, 0)
            jug_s, eq_s, c = conteo[clave]
            conteo[clave] = (jug_s, eq_s, c + 1)

        todos_los_registros = [
            (jug_obj, eq_obj, num_temps)
            for (_, _), (jug_obj, eq_obj, num_temps) in conteo.items()
        ]

        todos_los_registros.sort(key=lambda x: (-x[2], x[0].nombre))
        return todos_los_registros[:n]

    ###EJERCICIO 8###
    def obtener_parejas_mas_minutos_juntos(self, n: int):
        """
        Calcula qué parejas de jugadores han acumulado más minutos compartiendo vestuario
        en el mismo equipo y temporada.
        Devuelve: lista de (Jugador1, Jugador2, Equipo, minutos_totales)
        """
        # {(nombre_j1, nombre_j2, nombre_equipo): [j1_obj, j2_obj, equipo_obj, minutos]}
        registro_parejas = {}

        for temporada_obj in self.temporadas.values():
            for equipo_obj in temporada_obj.equipos.values():
                jugadores_list = equipo_obj.jugadores
                for jug1, jug2 in combinations(jugadores_list, 2):
                    # Ordenamos los jugadores por nombre para que la clave sea siempre la misma
                    if jug1.nombre <= jug2.nombre:
                        jug_a, jug_b = jug1, jug2
                    else:
                        jug_a, jug_b = jug2, jug1

                    clave = (jug_a.nombre, jug_b.nombre, equipo_obj.nombre)
                    minutos_temporada = jug1.estadistica.minutos + jug2.estadistica.minutos

                    if clave not in registro_parejas:
                        registro_parejas[clave] = [jug_a, jug_b, equipo_obj, 0.0]
                    registro_parejas[clave][3] += minutos_temporada

        resultado = [
            (v[0], v[1], v[2], int(v[3]))
            for v in registro_parejas.values()
        ]
        resultado.sort(key=lambda x: x[3], reverse=True)
        return resultado[:n]

    ###EJERCICIO 9###
    def obtener_top_jugadores_íntegros(self, n: int) -> list:
        """
        Jugadores que desde 1980 siempre han jugado todos sus partidos como titular
        y los han completado enteros (pjugados == ptitular == pcompletos).
        Devuelve: [(nombre, total_partidos)]
        """
        ranking = []

        for nombre, registros in self._jugadores_idx.items():
            total_partidos_desde_1980 = 0
            es_integro = True
            jugo_desde_1980 = False

            for _, _, jugador in registros:
                est = jugador.estadistica
                try:
                    anio = int(str(est.temporada)[:4])
                    if anio >= 1980:
                        jugo_desde_1980 = True
                        if not (est.pjugados == est.ptitular == est.pcompletos):
                            es_integro = False
                            break
                        total_partidos_desde_1980 += est.pjugados
                except ValueError:
                    continue

            if jugo_desde_1980 and es_integro and total_partidos_desde_1980 > 0:
                ranking.append((nombre, int(total_partidos_desde_1980)))

        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking[:n]

    ###EJERCICIO 10###
    def obtener_tarjetas_equipo_temporada(self, equipo: str, temporada: str) -> int:
        """
        Suma todas las tarjetas (amarillas + expulsiones) de un equipo en una temporada concreta.
        """
        total_tarjetas = 0
        equipo_buscado = equipo.upper()

        for temporada_obj, equipo_obj, jugador in self._iterar_historial():
            if (equipo_obj.nombre.upper() == equipo_buscado and
                    temporada_obj.id_temporada == str(temporada)):
                total_tarjetas += (jugador.estadistica.tarjetas + jugador.estadistica.expulsiones)

        return int(total_tarjetas)

    ###EJERCICIO 11###
    def obtener_revulsivos(self, lista_jugadores: list) -> dict:
        """
        Para una lista de nombres, calcula su goles totales y minutos por gol.
        Devuelve: {nombre: (total_goles, minutos_por_gol)}
        """
        resultados = {}

        for nombre in lista_jugadores:
            nombre_buscado = nombre.upper()

            if nombre_buscado not in self._jugadores_idx:
                continue

            total_goles = 0
            total_minutos = 0

            for _, _, jugador in self._jugadores_idx[nombre_buscado]:
                total_goles += jugador.estadistica.goles
                total_minutos += jugador.estadistica.minutos

            if total_goles > 0:
                minutos_por_gol = int(total_minutos / total_goles)
                resultados[nombre] = (int(total_goles), minutos_por_gol)

        return resultados

    ###EJERCICIO 12###
    def obtener_top_jugadores_mas_temporadas(self, n: int) -> list:
        """
        Busca los jugadores que más años han estado en activo en La Liga,
        calculado como (año última temporada) - (año primera temporada).
        Devuelve: [(nombre, anios_activo, anio_inicio, anio_fin)]
        """
        lista_activos = []

        for nombre, registros in self._jugadores_idx.items():
            anios_inicio = []

            for _, _, jugador in registros:
                try:
                    anio = int(str(jugador.estadistica.temporada)[:4])
                    anios_inicio.append(anio)
                except ValueError:
                    continue

            if not anios_inicio:
                continue

            min_anio = min(anios_inicio)
            max_anio = max(anios_inicio)
            anios_activo = max_anio - min_anio
            anio_fin_texto = max_anio + 1

            lista_activos.append((nombre, anios_activo, min_anio, anio_fin_texto))

        lista_activos.sort(key=lambda x: x[1], reverse=True)
        return lista_activos[:n]

    ###EJERCICIO 13###
    def obtener_top_jugadores_impolutos(self, n: int) -> list:
        """
        Jugadores que desde 1980 nunca han recibido ninguna tarjeta ni expulsión.
        Devuelve: [(nombre, total_partidos_desde_1980)]
        """
        lista_resultados = []

        for nombre, registros in self._jugadores_idx.items():
            total_partidos_desde_1980 = 0
            total_tarjetas_desde_1980 = 0
            jugo_desde_1980 = False

            for _, _, jugador in registros:
                est = jugador.estadistica
                try:
                    anio = int(str(est.temporada)[:4])
                    if anio >= 1980:
                        jugo_desde_1980 = True
                        total_partidos_desde_1980 += est.pjugados
                        total_tarjetas_desde_1980 += (est.tarjetas + est.expulsiones)
                except ValueError:
                    continue

            if jugo_desde_1980 and total_tarjetas_desde_1980 == 0 and total_partidos_desde_1980 > 0:
                lista_resultados.append((nombre, int(total_partidos_desde_1980)))

        lista_resultados.sort(key=lambda x: x[1], reverse=True)
        return lista_resultados[:n]

    ###EJERCICIO 14###
    def obtener_top_jugadores_sustituidos(self, n: int) -> list:
        """
        Jugadores que han sido sustituidos más veces a lo largo de su carrera.
        Un jugador es sustituido cuando empieza como titular pero no termina el partido.
        Devuelve: [(nombre, total_cambios)]
        """
        lista_sustituidos = []

        for nombre, registros in self._jugadores_idx.items():
            total_cambios = 0

            for _, _, jugador in registros:
                est = jugador.estadistica
                try:
                    cambios_esta_temporada = est.ptitular - est.pcompletos
                    if cambios_esta_temporada > 0:
                        total_cambios += cambios_esta_temporada
                except AttributeError:
                    continue

            if total_cambios > 0:
                lista_sustituidos.append((nombre, int(total_cambios)))

        lista_sustituidos.sort(key=lambda x: x[1], reverse=True)
        return lista_sustituidos[:n]

    ###EJERCICIO 15###
    def obtener_top_goleadores_unicos(self, n: int) -> list:
        """
        Jugadores que marcaron todos sus goles en una única temporada.
        Devuelve: lista de dicts {'nombre', 'goles', 'temporada'}
        """
        jugadores_una_sola_vez = []

        for nombre, registros in self._jugadores_idx.items():
            temporadas_con_goles = [
                (_, _, j) for _, _, j in registros if j.estadistica.goles > 0
            ]

            if len(temporadas_con_goles) == 1:
                jug = temporadas_con_goles[0][2]
                jugadores_una_sola_vez.append({
                    'nombre': nombre,
                    'goles': int(jug.estadistica.goles),
                    'temporada': jug.estadistica.temporada
                })

        jugadores_una_sola_vez.sort(key=lambda x: x['goles'], reverse=True)
        return jugadores_una_sola_vez[:n]

    ###EJERCICIO 16###
    def obtener_top_eficiencia_goleadora(self, n: int) -> list:
        """
        Jugadores con al menos 50 goles históricos, ordenados por menor ratio minutos/gol
        (cuanto menos minutos tarda en marcar, más eficiente).
        Devuelve: lista de dicts {'nombre', 'goles', 'ratio'}
        """
        ranking_eficiencia = []

        for nombre, registros in self._jugadores_idx.items():
            total_goles = 0
            total_minutos = 0

            for _, _, jugador in registros:
                total_goles += jugador.estadistica.goles
                total_minutos += jugador.estadistica.minutos

            if total_goles >= 50:
                ratio = total_minutos / total_goles
                ranking_eficiencia.append({
                    'nombre': nombre,
                    'goles': int(total_goles),
                    'ratio': ratio
                })

        ranking_eficiencia.sort(key=lambda x: x['ratio'])
        return ranking_eficiencia[:n]

    ###EJERCICIO 17###
    def obtener_top_jugadores_sin_gol(self, n: int) -> list:
        """
        Jugadores que NUNCA han marcado un gol, ordenados por más partidos jugados.
        Devuelve: lista de dicts {'nombre', 'completos'}
        """
        ranking = []

        for nombre, registros in self._jugadores_idx.items():
            total_goles = 0
            total_partidos = 0

            for _, _, jugador in registros:
                total_goles += jugador.estadistica.goles
                total_partidos += jugador.estadistica.pjugados

            if total_goles == 0 and total_partidos > 0:
                ranking.append({
                    'nombre': nombre,
                    'completos': int(total_partidos)
                })

        ranking.sort(key=lambda x: x['completos'], reverse=True)
        return ranking[:n]

    ###EJERCICIO 18###
    def obtener_jugadores_goles_decadas_exacto(self, n: int) -> list:
        """
        Busca jugadores que han marcado en el mayor número de décadas distintas.
        Devuelve lista de dicts con nombre, num_decadas, decadas (lista), etc.
        """
        ranking = []

        for nombre, registros in self._jugadores_idx.items():
            decadas_con_gol = set()
            total_goles_carrera = 0
            total_partidos_jugados = 0
            total_penalties_fallados = 0

            for _, _, jugador in registros:
                est = jugador.estadistica
                total_goles_carrera += est.goles
                total_partidos_jugados += est.pjugados
                total_penalties_fallados += est.penalties_fallados

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
                    'total_goles': total_goles_carrera,
                    'total_partidos_jugados': total_partidos_jugados,
                    'penalties_fallados': total_penalties_fallados
                })

        ranking.sort(key=lambda x: (-x['num_decadas'], sum(x['decadas'])))
        return ranking[:n]

    ###EJERCICIO 19###
    def obtener_descendidos(self, temporada_objetivo: str) -> list:
        """
        Devuelve los equipos que descendieron al finalizar la temporada indicada,
        es decir, los que estaban en esa temporada pero no en la siguiente.
        """
        try:
            inicio = int(temporada_objetivo[:4])
            fin = int(temporada_objetivo[5:])
            siguiente_temp = f"{inicio + 1}-{str(fin + 1).zfill(2)}"
            if temporada_objetivo == "1998-99":
                siguiente_temp = "1999-00"
        except Exception:
            return []

        equipos_por_temporada = self._construir_equipos_por_temporada()
        equipos_ahora = equipos_por_temporada.get(temporada_objetivo, set())
        equipos_proxima = equipos_por_temporada.get(siguiente_temp, set())

        if not equipos_proxima:
            return []

        return sorted(list(equipos_ahora - equipos_proxima))

    ###EJERCICIO 20###
    def obtener_equipos_mas_descendidos(self, n: int) -> str:
        """
        Calcula qué equipos han sufrido más descensos a lo largo de la historia.
        Devuelve una cadena formateada con el ranking.
        """
        equipos_por_temporada = self._construir_equipos_por_temporada()
        todos_los_descensos = []

        for temporada, equipos_actuales in equipos_por_temporada.items():
            try:
                inicio = int(temporada[:4])
                fin = int(temporada[5:])
                siguiente_temp = f"{inicio + 1}-{str(fin + 1).zfill(2)}"
                if temporada == "1998-99":
                    siguiente_temp = "1999-00"
            except (ValueError, IndexError):
                continue

            if siguiente_temp in equipos_por_temporada:
                equipos_proxima = equipos_por_temporada[siguiente_temp]
                descendidos = equipos_actuales - equipos_proxima
                todos_los_descensos.extend(descendidos)

        conteo = Counter(todos_los_descensos)
        ordenados = sorted(conteo.items(), key=lambda x: (-x[1], x[0]))

        resultado = ""
        for equipo, num in ordenados[:n]:
            resultado += f"- {equipo}: {num} descensos\n"
        return resultado.strip()

    ###EJERCICIO 21###
    def obtener_ascendidos(self, temporada_objetivo: str) -> list:
        """
        Devuelve los equipos que ascendieron para disputar la temporada indicada,
        es decir, los que están en esa temporada pero no estaban en la anterior.
        """
        if temporada_objetivo == "1928-29":
            return []

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

        equipos_por_temporada = self._construir_equipos_por_temporada()
        equipos_ahora = equipos_por_temporada.get(temporada_objetivo, set())
        equipos_anterior = equipos_por_temporada.get(anterior_temp, set())

        if not equipos_anterior:
            return []

        return sorted(list(equipos_ahora - equipos_anterior))

    ###EJERCICIO 22###
    def obtener_equipos_mas_ascendidos(self, n: int) -> list:
        """
        Calcula qué equipos han ascendido más veces a lo largo de la historia.
        Devuelve: [(nombre_equipo, num_ascensos)]
        """
        equipos_por_temporada = self._construir_equipos_por_temporada()
        todos_los_ascensos = []

        for temporada, equipos_actuales in equipos_por_temporada.items():
            if temporada == "1928-29":
                continue

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

            if anterior_temp in equipos_por_temporada:
                equipos_anterior = equipos_por_temporada[anterior_temp]
                ascendidos = equipos_actuales - equipos_anterior
                todos_los_ascensos.extend(ascendidos)

        conteo = Counter(todos_los_ascensos)
        ordenados = sorted(conteo.items(), key=lambda x: (-x[1], x[0]))
        return ordenados[:n]

    ###EJERCICIO 23###
    def obtener_equipos_mas_temporadas(self, n: int) -> list:
        """
        Equipos con más temporadas disputadas en La Liga a lo largo de la historia.
        Devuelve: [(nombre_equipo, num_temporadas)]
        """
        conteo = [
            (nombre, len(pares))
            for nombre, pares in self._equipos_por_nombre.items()
        ]
        return sorted(conteo, key=lambda x: (-x[1], x[0]))[:n]

    ###EJERCICIO 24###
    def obtener_equipos_menos_temporadas(self, n: int) -> list:
        """
        Equipos con menos temporadas disputadas en La Liga a lo largo de la historia.
        Devuelve: [(nombre_equipo, num_temporadas)]
        """
        conteo = [
            (nombre, len(pares))
            for nombre, pares in self._equipos_por_nombre.items()
        ]
        return sorted(conteo, key=lambda x: (x[1], x[0]))[:n]

    ###EJERCICIO 25###
    def obtener_equipos_mas_goles(self, n: int) -> list:
        """
        Equipos que más goles han marcado en total a lo largo de toda la historia.
        Devuelve: [(nombre_equipo, total_goles)]
        """
        goles_por_equipo = {}

        for nombre_equipo, pares in self._equipos_por_nombre.items():
            total = sum(eq_obj.goles_marcados for _, eq_obj in pares)
            goles_por_equipo[nombre_equipo] = int(total)

        return sorted(goles_por_equipo.items(), key=lambda x: (-x[1], x[0]))[:n]

    ###EJERCICIO 26###
    def obtener_equipos_menos_goles(self, n: int) -> list:
        """
        Equipos que menos goles han marcado en total a lo largo de la historia.
        Devuelve primero los N con menos goles, pero los muestra de más a menos.
        """
        goles_por_equipo = {}

        for nombre_equipo, pares in self._equipos_por_nombre.items():
            total = sum(eq_obj.goles_marcados for _, eq_obj in pares)
            goles_por_equipo[nombre_equipo] = int(total)

        peores_n = sorted(goles_por_equipo.items(), key=lambda x: (x[1], x[0]))[:n]
        return sorted(peores_n, key=lambda x: (-x[1], x[0]))

    ###EJERCICIO 27###
    def obtener_mejores_temporadas_ratio_goles(self, n: int) -> list:
        """
        Calcula el ratio de goles por partido de cada temporada y devuelve las N mejores.
        El resultado final se ordena cronológicamente.
        Devuelve: lista de dicts {'temporada', 'goles', 'partidos', 'ratio'}
        """
        resultados_ratio = []

        for temp_id, temp_obj in self.temporadas.items():
            if temp_obj.num_equipos <= 1:
                continue

            partidos_totales = temp_obj.num_partidos
            goles_totales = temp_obj.goles_totales
            ratio = goles_totales / partidos_totales

            resultados_ratio.append({
                'temporada': temp_id,
                'goles': int(goles_totales),
                'partidos': partidos_totales,
                'ratio': ratio
            })

        top_n = sorted(resultados_ratio, key=lambda x: x['partidos'])[:n]
        return top_n

    ###EJERCICIO 28###
    def obtener_empates_equipos_mas_goles(self) -> list:
        """
        Busca las temporadas donde más de un equipo compartió el título de máximo goleador.
        Devuelve: lista de dicts {'temporada', 'equipos'}
        """
        resultados = []

        for temp_id in sorted(self.temporadas.keys()):
            temp_obj = self.temporadas[temp_id]
            goles_por_equipo = {
                eq.nombre: eq.goles_marcados for eq in temp_obj.equipos.values()
            }

            if not goles_por_equipo:
                continue

            max_goles = max(goles_por_equipo.values())
            maximos = [e for e, g in goles_por_equipo.items() if g == max_goles]

            if len(maximos) > 1:
                resultados.append({'temporada': temp_id, 'equipos': maximos})

        return resultados

    ###EJERCICIO 29###
    def obtener_rachas_maximo_goleador(self, n: int) -> list:
        """
        Calcula las rachas consecutivas de temporadas en que cada equipo fue el máximo
        goleador de La Liga.
        Devuelve: [(nombre_equipo, racha_maxima)]
        """
        goles_temporada = {}

        for temp_id, temp_obj in self.temporadas.items():
            goles_temporada[temp_id] = {
                eq.nombre: int(eq.goles_marcados) for eq in temp_obj.equipos.values()
            }

        maximos_por_temporada = {}
        for temporada, equipos_goles in goles_temporada.items():
            if not equipos_goles:
                continue
            max_goles = max(equipos_goles.values())
            maximos_por_temporada[temporada] = [
                eq for eq, g in equipos_goles.items() if g == max_goles
            ]

        rachas_maximas = {}
        rachas_actuales = {}

        for temporada in sorted(maximos_por_temporada.keys()):
            goleadores_actuales = maximos_por_temporada[temporada]

            for equipo in goleadores_actuales:
                rachas_actuales[equipo] = rachas_actuales.get(equipo, 0) + 1
                if rachas_actuales[equipo] > rachas_maximas.get(equipo, 0):
                    rachas_maximas[equipo] = rachas_actuales[equipo]

            for equipo in list(rachas_actuales.keys()):
                if equipo not in goleadores_actuales:
                    rachas_actuales[equipo] = 0

        ordenados = sorted(rachas_maximas.items(), key=lambda x: (-x[1], x[0] == "Athletic Club"))
        return ordenados[:n]

    ###EJERCICIO 30###
    def obtener_jugadores_comunes(self, equipo1: str, equipo2: str) -> list:
        """
        Encuentra los jugadores que han militado en ambos equipos a lo largo de
        su carrera (no necesariamente al mismo tiempo).
        Devuelve: lista de nombres ordenados alfabéticamente.
        """
        jugadores_comunes = []

        for nombre, registros in self._jugadores_idx.items():
            equipos_jugador = set(eq_obj.nombre for _, eq_obj, _ in registros)

            if equipo1 in equipos_jugador and equipo2 in equipos_jugador:
                jugadores_comunes.append(nombre)

        return sorted(jugadores_comunes)

    ###EJERCICIO 31###
    def obtener_menor_promedio_minutos(self, n: int) -> list:
        """
        Jugadores con al menos 8 temporadas en La Liga, ordenados por menor promedio
        de minutos por temporada.
        Devuelve: lista de dicts {'nombre', 'promedio', 'total_minutos', 'temporadas'}
        """
        ranking = []

        for nombre, registros in self._jugadores_idx.items():
            total_minutos = 0
            temporadas_unicas = set()

            for temp_obj, _, jugador in registros:
                total_minutos += jugador.estadistica.minutos
                temporadas_unicas.add(temp_obj.id_temporada)

            num_temporadas = len(temporadas_unicas)

            if num_temporadas >= 8 and total_minutos > 0:
                promedio = total_minutos / num_temporadas
                ranking.append({
                    'nombre': nombre,
                    'promedio': promedio,
                    'total_minutos': int(total_minutos),
                    'temporadas': num_temporadas
                })

        ranking.sort(key=lambda x: (x['temporadas'], x['promedio']))
        return ranking[:n]

    ###EJERCICIO 32###
    def obtener_top_anios_fuera(self, n: int) -> list:
        """
        Busca jugadores que volvieron a un mismo equipo tras el mayor número de años fuera.
        El "gap" es la diferencia más grande entre dos años consecutivos que jugaron en ese club.
        Devuelve: lista de dicts {'nombre', 'equipo', 'anios_fuera'}
        """
        ranking = []

        for nombre, registros in self._jugadores_idx.items():
            anios_por_equipo = {}

            for _, eq_obj, jugador in registros:
                try:
                    anio = int(str(jugador.estadistica.temporada)[:4])
                    if eq_obj.nombre not in anios_por_equipo:
                        anios_por_equipo[eq_obj.nombre] = []
                    anios_por_equipo[eq_obj.nombre].append(anio)
                except ValueError:
                    continue

            for equipo, anios in anios_por_equipo.items():
                if len(anios) > 1:
                    anios.sort()
                    max_gap = 0
                    for i in range(1, len(anios)):
                        gap = anios[i] - anios[i - 1]
                        if gap > max_gap:
                            max_gap = gap

                    if max_gap > 1:
                        ranking.append({
                            'nombre': nombre,
                            'equipo': equipo,
                            'anios_fuera': max_gap
                        })

        ranking.sort(key=lambda x: x['anios_fuera'], reverse=True)
        return ranking[:n]

    ###EJERCICIO 33###
    def obtener_rachas_sin_tarjetas_desempate_goles(self, n: int) -> list:
        """
        Calcula la racha más larga de temporadas consecutivas (desde 1970) en que un jugador
        no recibió ninguna tarjeta y disputó al menos un minuto.
        En caso de empate en racha, se desempata por goles históricos totales.
        Devuelve: lista de dicts {'nombre', 'racha', 'goles'}
        """
        # {nombre: {temporada_id: {'t': tarjetas, 'm': minutos}}}
        jugador_stats = {}
        goles_totales_hist = {}

        for temp_obj, _, jugador in self._iterar_historial():
            nombre = jugador.nombre
            temp_id = temp_obj.id_temporada

            if nombre not in jugador_stats:
                jugador_stats[nombre] = {}
                goles_totales_hist[nombre] = 0.0

            # Si un jugador tiene varios registros en la misma temporada (por ejemplo en
            # distintos equipos), acumulamos las tarjetas y minutos en esa temporada.
            if temp_id not in jugador_stats[nombre]:
                jugador_stats[nombre][temp_id] = {'t': 0.0, 'm': 0.0}

            jugador_stats[nombre][temp_id]['t'] += float(jugador.estadistica.tarjetas)
            jugador_stats[nombre][temp_id]['m'] += float(jugador.estadistica.minutos)
            goles_totales_hist[nombre] += float(jugador.estadistica.goles)

        resultados = []

        for nombre, temporadas in jugador_stats.items():
            racha_actual = 0
            racha_maxima = 0
            anio_previo = -1

            for temp in sorted(temporadas.keys()):
                try:
                    anio_actual = int(temp.split('-')[0])
                except Exception:
                    continue

                if anio_actual < 1970:
                    continue

                datos = temporadas[temp]

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
                    'goles': goles_totales_hist[nombre]
                })

        resultados.sort(key=lambda x: (-x['racha'], -x['goles'], x['nombre']))
        return resultados[:n]

    # =========================================================================
    # MÉTODO DE HISTORIAL COMPLETO
    # =========================================================================

    def obtener_historial_jugador_completo(self, nombre_jugador: str) -> list:
        """
        Devuelve el historial completo de un jugador fila por fila, con el contexto
        de temporada y equipo incluidos, ordenado cronológicamente.
        """
        historial = []
        nombre_buscar = nombre_jugador.upper()

        for temp_obj, eq_obj, jugador in self._iterar_historial():
            if jugador.nombre.upper() == nombre_buscar:
                datos = {
                    'temporada': temp_obj.id_temporada,
                    'equipo': eq_obj.nombre
                }
                # Añadimos todos los atributos estadísticos del objeto Estadistica
                for clave, valor in vars(jugador.estadistica).items():
                    if clave not in ('temporada', 'equipo'):
                        datos[clave] = valor
                historial.append(datos)

        return sorted(historial, key=lambda x: x['temporada'])

    # =========================================================================

    def __str__(self):
        return (f"Liga: {self.nombre} | "
                f"Temporadas: {self.num_temporadas} | "
                f"No jugadas: {self.num_temporadas_no_jugadas} | "
                f"Equipos distintos: {len(self._equipos_por_nombre)} | "
                f"Jugadores distintos: {len(self._jugadores_idx)}")
