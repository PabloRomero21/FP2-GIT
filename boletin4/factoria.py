import pandas as pd
from jugador import Jugador
from estadistica import Estadistica

class FactoriaJugadores:
    """
    Clase Factoría sin estado persistente. 
    Su única responsabilidad es procesar el archivo Excel y devolver una lista de objetos Jugador.
    """

    @staticmethod
    def _extraer_anio(temporada: str) -> int:
        """
        Extrae el año inicial de la temporada (ej: '1928-29' -> 1928).
        Al ser @staticmethod, funciona como una simple función de utilidad dentro de la clase.
        """
        try:
            return int(str(temporada).split('-')[0])
        except (ValueError, AttributeError):
            return 0

    @classmethod
    def _obtener_ultima_temporada(cls, jugador) -> int:
        if not jugador.estadisticas:
            return 0
        
        # AQUÍ ESTABA EL ERROR: 
        # Iteramos directamente sobre la lista 'jugador.estadisticas', sin usar .keys()
        anios = [cls._extraer_anio(est.temporada) for est in jugador.estadisticas]
        return max(anios)

    @classmethod
    def crear_jugadores_desde_excel(cls, ruta_archivo: str) -> list:
        """
        Lee el archivo .xls, agrupa la información y devuelve una LISTA de objetos Jugador.
        """
        LIMITE_SALTO_ANIOS = 20
        jugadores_temp = {}
        
        df = pd.read_excel(ruta_archivo)
        df = df.fillna(0.0)

        for index, fila in df.iterrows():
            nombre_base = str(fila['JUGADOR']).strip()
            temporada = str(fila['TEMPORADA']).strip()
            equipo = str(fila['EQUIPO']).strip()
            
            anio_actual = cls._extraer_anio(temporada)
            
            # --- NUEVO CONTROL DE HOMÓNIMOS MEJORADO ---
            nombre_clave = nombre_base
            sufijo = 0
            
            # Buscamos la "versión" correcta de este jugador
            while nombre_clave in jugadores_temp:
                jugador_existente = jugadores_temp[nombre_clave]
                ultimo_anio_registrado = cls._obtener_ultima_temporada(jugador_existente)
                
                # Si el salto de años es menor al límite, es el mismo jugador. Paramos de buscar.
                if abs(anio_actual - ultimo_anio_registrado) < LIMITE_SALTO_ANIOS:
                    break 
                else:
                    # Si el salto es muy grande, probamos con el siguiente sufijo
                    sufijo += 1
                    nombre_clave = f"{nombre_base}_duplicado_{sufijo}"

            # Si después de buscar, esta clave no existe, es que es un jugador nuevo (original o duplicado nuevo)
            if nombre_clave not in jugadores_temp:
                # Si el sufijo es mayor a 0, significa que hemos tenido que crear un duplicado
                if sufijo > 0:
                    print(f"Precaución: homónimo detectado para {nombre_base}. Registrado como {nombre_clave}")
                
                jugadores_temp[nombre_clave] = Jugador(nombre_clave)

            # Extraemos y asignamos las estadísticas al jugador correcto
            jugadores_temp[nombre_clave].agregar_estadisticas(
                temporada=temporada,
                equipo=equipo,
                pjugados=float(fila['PJUGADOS']),
                pcompletos=float(fila['PCOMPLETOS']),
                ptitular=float(fila['PTITULAR']),
                psuplente=float(fila['PSUPLENTE']),
                minutos=float(fila['MINUTOS']),
                lesiones=float(fila['LESIONES']),
                tarjetas=float(fila['TARJETAS']),
                expulsiones=float(fila['EXPULSIONES']),
                goles=float(fila['GOLES']),
                penalties_fallados=float(fila['PENALTIES FALLADOS'])
            )
                
        return list(jugadores_temp.values())