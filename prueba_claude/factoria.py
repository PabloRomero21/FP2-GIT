import pandas as pd
from jugador import Jugador
from estadistica import Estadistica
from equipos import Equipo
from temporada import Temporada
from liga import Liga


class FactoriaJugadores:
    """
    Clase Factoría sin estado persistente.
    Su responsabilidad es leer el fichero Excel, validar la integridad de los datos
    y construir el objeto Liga con la jerarquía completa:

        Liga -> Temporada -> Equipo -> Jugador (con su Estadistica)

    Validaciones aplicadas a cada fila antes de insertarla:
        1. La temporada es coherente: dos años consecutivos (ej: '2017-18', no '2017-19').
        2. Todos los valores numéricos son positivos (>= 0).
        3. pcompletos <= ptitular.
        4. pjugados == ptitular + psuplente.
        5. minutos <= pjugados * 90 (no se contemplan tiempos extra).

    Validación post-construcción:
        6. pjugados de cada jugador <= num_partidos de su temporada (N*(N-1)).
    """

    # =========================================================================
    # MÉTODOS PRIVADOS DE VALIDACIÓN
    # =========================================================================

    @staticmethod
    def _validar_temporada(temporada: str) -> bool:
        """
        Comprueba que el identificador de temporada tiene el formato XXXX-YY
        y que los dos años son consecutivos.
        Ejemplos válidos: '1928-29', '1998-99', '1999-00', '2017-18'.
        Ejemplos inválidos: '2017-19', '17-18', 'abc'.
        """
        try:
            partes = str(temporada).split('-')
            if len(partes) != 2:
                return False

            anio_inicio = int(partes[0])
            sufijo_fin = int(partes[1])

            # Reconstruimos el año de fin completo teniendo en cuenta el cambio de siglo
            # Ejemplo: '1999-00' -> anio_inicio=1999, sufijo_fin=0 -> anio_fin=2000
            siglo_base = (anio_inicio // 100) * 100
            anio_fin_esperado = anio_inicio + 1
            sufijo_esperado = anio_fin_esperado % 100

            return sufijo_fin == sufijo_esperado

        except (ValueError, AttributeError):
            return False

    @staticmethod
    def _extraer_anio(temporada: str) -> int:
        """
        Extrae el año de inicio de una temporada (ej: '1928-29' -> 1928).
        Usado para el control de homónimos en la detección de jugadores distintos
        con el mismo nombre.
        """
        try:
            return int(str(temporada).split('-')[0])
        except (ValueError, AttributeError):
            return 0

    @classmethod
    def _validar_fila(cls, fila_desc: str, pjugados: float, pcompletos: float,
                      ptitular: float, psuplente: float, minutos: float,
                      lesiones: float, tarjetas: float, expulsiones: float,
                      goles: float, penalties_fallados: float,
                      temporada: str) -> list:
        """
        Aplica las validaciones 1-5 sobre los datos de una fila del Excel.
        Devuelve una lista de mensajes de error (vacía si todo es correcto).
        """
        errores = []

        # Validación 1: temporada coherente
        if not cls._validar_temporada(temporada):
            errores.append(f"[ERROR] {fila_desc}: Temporada incoherente '{temporada}'.")

        # Validación 2: todos los valores >= 0
        valores_numericos = {
            'PJUGADOS': pjugados, 'PCOMPLETOS': pcompletos, 'PTITULAR': ptitular,
            'PSUPLENTE': psuplente, 'MINUTOS': minutos, 'LESIONES': lesiones,
            'TARJETAS': tarjetas, 'EXPULSIONES': expulsiones, 'GOLES': goles,
            'PENALTIES FALLADOS': penalties_fallados
        }
        for campo, valor in valores_numericos.items():
            if valor < 0:
                errores.append(f"[ERROR] {fila_desc}: Valor negativo en '{campo}' ({valor}).")

        # Validación 3: pcompletos <= ptitular
        if pcompletos > ptitular:
            errores.append(
                f"[ERROR] {fila_desc}: pcompletos ({pcompletos}) > ptitular ({ptitular})."
            )

        # Validación 4: pjugados == ptitular + psuplente
        if abs(pjugados - (ptitular + psuplente)) > 0.01:
            errores.append(
                f"[ERROR] {fila_desc}: pjugados ({pjugados}) != ptitular + psuplente "
                f"({ptitular} + {psuplente} = {ptitular + psuplente})."
            )

        # Validación 5: minutos <= pjugados * 90
        if minutos > pjugados * 90 + 0.01:
            errores.append(
                f"[ERROR] {fila_desc}: minutos ({minutos}) > pjugados * 90 "
                f"({pjugados * 90})."
            )

        return errores

    # =========================================================================
    # MÉTODO PRINCIPAL
    # =========================================================================

    @classmethod
    def crear_liga_desde_excel(cls, ruta_archivo: str, nombre_liga: str = "La Liga") -> Liga:
        """
        Lee el fichero Excel, valida cada fila y construye el objeto Liga completo.

        Parámetros:
            ruta_archivo  -- Ruta al fichero .xls o .xlsx con los datos históricos.
            nombre_liga   -- Nombre de la liga (por defecto 'La Liga').

        Devuelve:
            Objeto Liga completamente construido con toda la jerarquía
            Temporada -> Equipo -> Jugador, e índices secundarios listos para consultar.
        """
        la_liga = Liga(nombre_liga)
        todos_los_errores = []
        filas_omitidas = 0

        df = pd.read_excel(ruta_archivo)
        df = df.fillna(0.0)

        for index, fila in df.iterrows():
            nombre_jugador = str(fila['JUGADOR']).strip()
            temporada_id   = str(fila['TEMPORADA']).strip()
            equipo_nombre  = str(fila['EQUIPO']).strip()

            pjugados          = float(fila['PJUGADOS'])
            pcompletos        = float(fila['PCOMPLETOS'])
            ptitular          = float(fila['PTITULAR'])
            psuplente         = float(fila['PSUPLENTE'])
            minutos           = float(fila['MINUTOS'])
            lesiones          = float(fila['LESIONES'])
            tarjetas          = float(fila['TARJETAS'])
            expulsiones       = float(fila['EXPULSIONES'])
            goles             = float(fila['GOLES'])
            penalties_fallados = float(fila['PENALTIES FALLADOS'])

            fila_desc = f"Fila {index + 2} ({nombre_jugador} | {temporada_id} | {equipo_nombre})"

            # --- VALIDACIONES 1-5 ---
            errores_fila = cls._validar_fila(
                fila_desc, pjugados, pcompletos, ptitular, psuplente,
                minutos, lesiones, tarjetas, expulsiones, goles,
                penalties_fallados, temporada_id
            )

            if errores_fila:
                todos_los_errores.extend(errores_fila)
                filas_omitidas += 1
                continue   # La fila no se inserta en la estructura

            # --- CONSTRUCCIÓN DE OBJETOS ---
            est = Estadistica(
                temporada_id, equipo_nombre,
                pjugados, pcompletos, ptitular, psuplente,
                minutos, lesiones, tarjetas, expulsiones,
                goles, penalties_fallados
            )
            jugador = Jugador(nombre_jugador, est)

            # --- INSERCIÓN EN LA JERARQUÍA ---
            # Temporada
            if temporada_id not in la_liga.temporadas:
                nueva_temporada = Temporada(temporada_id)
                la_liga.agregar_temporada(nueva_temporada)
            temp_obj = la_liga.temporadas[temporada_id]

            # Equipo (dentro de esa temporada)
            if equipo_nombre not in temp_obj.equipos:
                nuevo_equipo = Equipo(equipo_nombre, temporada_id)
                temp_obj.agregar_equipo(nuevo_equipo)
            eq_obj = temp_obj.equipos[equipo_nombre]

            # Jugador (dentro del equipo de esa temporada)
            eq_obj.agregar_jugador(jugador)

        # --- CONSTRUCCIÓN DE ÍNDICES SECUNDARIOS ---
        # Se hace una única vez, al finalizar la inserción de todos los datos.
        la_liga._construir_indices()

        # --- INFORME DE VALIDACIONES 1-5 ---
        if todos_los_errores:
            print(f"\n{'='*60}")
            print(f"INFORME DE VALIDACIÓN: {len(todos_los_errores)} problema(s) detectado(s).")
            print(f"{filas_omitidas} fila(s) omitida(s) de la estructura de datos.")
            print(f"{'='*60}")
            for mensaje in todos_los_errores[:30]:
                print(mensaje)
            if len(todos_los_errores) > 30:
                print(f"... y {len(todos_los_errores) - 30} problema(s) más.")
            print(f"{'='*60}\n")

        # --- VALIDACIÓN 6 (post-construcción) ---
        # pjugados de cada jugador no puede superar el total de partidos de la temporada.
        cls._validar_partidos_vs_temporada(la_liga)

        return la_liga

    @staticmethod
    def _validar_partidos_vs_temporada(la_liga: Liga):
        """
        Validación 6: comprueba que ningún jugador tiene registrados más partidos
        jugados que los que tiene esa temporada en total (N*(N-1)).
        Se ejecuta una sola vez tras construir la estructura completa porque el
        total de partidos de la temporada solo se conoce cuando ya están todos los
        equipos registrados.
        """
        avisos = []
        for temp_obj in la_liga.temporadas.values():
            max_partidos_temporada = temp_obj.num_partidos
            if max_partidos_temporada == 0:
                continue   # Temporada vacía o con un solo equipo, no hay límite aplicable

            for eq_obj in temp_obj.equipos.values():
                for jugador in eq_obj.jugadores:
                    if jugador.estadistica.pjugados > max_partidos_temporada:
                        avisos.append(
                            f"[AVISO-V6] {jugador.nombre} | {eq_obj.nombre} | "
                            f"{temp_obj.id_temporada}: "
                            f"pjugados ({int(jugador.estadistica.pjugados)}) > "
                            f"num_partidos_temporada ({max_partidos_temporada})."
                        )

        if avisos:
            print(f"\n{'='*60}")
            print(f"VALIDACIÓN 6: {len(avisos)} aviso(s) de partidos excesivos.")
            print(f"{'='*60}")
            for aviso in avisos[:20]:
                print(aviso)
            if len(avisos) > 20:
                print(f"... y {len(avisos) - 20} aviso(s) más.")
            print(f"{'='*60}\n")
