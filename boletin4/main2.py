from factoria import FactoriaJugadores
import os
import pickle
from liga import Liga

def main():
    # --- CONFIGURACIÓN DE RUTAS Y CARGA ---
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_xls = os.path.join(directorio_actual, "Plantillas1D-2017-18.xls")
    ruta_pkl = os.path.join(directorio_actual, "liga_completa.pkl")
    
    la_liga = None

    if os.path.exists(ruta_pkl):
        print(f"SISTEMA: Cargando LIGA COMPLETA desde: {ruta_pkl}...")
        with open(ruta_pkl, 'rb') as archivo_entrada:
            la_liga = pickle.load(archivo_entrada)
        print("SISTEMA: ¡Datos cargados con éxito!\n")
    else:
        print("SISTEMA: Procesando Excel (esto puede tardar unos segundos)...")
        lista_jugadores = FactoriaJugadores.crear_jugadores_desde_excel(ruta_xls)
        la_liga = Liga("La Liga Santander", lista_jugadores)
        
        print("SISTEMA: Guardando copia de seguridad...")
        with open(ruta_pkl, 'wb') as archivo_salida:
            pickle.dump(la_liga, archivo_salida)
        print("SISTEMA: Estructura creada y guardada.\n")    

    # --- EJERCICIO 1: Máximo Goleador en una Temporada ---
    print("--- EJERCICIO 1 (MÁXIMO GOLEADOR TEMPORADA) ---")
    maximo_goleador_temporada = la_liga.obtener_maximo_goleador_temporada()
    jugador_obj = maximo_goleador_temporada[0]
    est_obj = maximo_goleador_temporada[1]
    print(f"- {jugador_obj.nombre} ({est_obj.equipo} - Temporada {est_obj.temporada}) | Partidos: {int(est_obj.pjugados)} | Goles: {int(est_obj.goles)}\n")


    # --- EJERCICIO 2: Máximo Goleador Histórico ---
    print("--- EJERCICIO 2 (MÁXIMO GOLEADOR HISTÓRICO) ---")
    maximo_historico = la_liga.obtener_maximo_goleador_historico()
    jugador_hist_obj = maximo_historico[0]
    total_goles = maximo_historico[1]
    print(f"- {jugador_hist_obj.nombre}: {int(total_goles)} goles totales.\n")


    # --- EJERCICIO 3: Jugador Trotamundos ---
    print("--- EJERCICIO 3 (JUGADOR TROTAMUNDOS) ---")
    resultado_trotamundos = la_liga.obtener_jugador_mas_equipos()
    jugador_trotamundos = resultado_trotamundos[0]
    lista_equipos = resultado_trotamundos[1]
    print(f"- {jugador_trotamundos.nombre} - Equipos: {', '.join(lista_equipos)}\n")


    # --- EJERCICIO 4: Récord Partidos en un Club ---
    print("--- EJERCICIO 4 (RÉCORD PARTIDOS EN UN CLUB) ---")
    resultado_record = la_liga.obtener_jugador_record_partidos_en_un_club()
    jugador_rec = resultado_record[0]
    equipo_nome, partidos_num = resultado_record[1]
    print(f"- {jugador_rec.nombre} - Equipo: {equipo_nome}, Partidos: {partidos_num}\n")   


    # --- EJERCICIO 5: Minutos Totales ---
    print("--- EJERCICIO 5 (MÁXIMOS MINUTOS JUGADOS) ---")
    jugador_minutos_obj, minutos_totales = la_liga.obtener_jugador_mas_minutos_total()
    print(f"- {jugador_minutos_obj.nombre} con un total de {minutos_totales} minutos jugados.\n")


    # --- EJERCICIO 6: Consulta de Clubes por Jugador ---
    print("--- EJERCICIO 6 (CONSULTA DE CLUBES) ---")
    jugadores_consulta = ["JULIO SALINAS", "SALVA B.", "ARIZMENDI"]
    for nombre in jugadores_consulta:
        objetos_equipo = la_liga.obtener_objetos_equipo_jugador(nombre)
        if objetos_equipo:
            nombres_de_clubes = [eq.nombre for eq in objetos_equipo]
            print(f"- {nombre}: {', '.join(nombres_de_clubes)}")
        else:
            print(f"- {nombre}: No se han encontrado datos.")
    print("\n")


    # --- EJERCICIO 7: Jugadores Fieles ---
    print("--- EJERCICIO 7 (TOP JUGADORES FIELES) ---")
    top_fieles = la_liga.obtener_top_jugadores_fieles(5)
    for (jug, eq, temps) in top_fieles:
        print(f"- {jug.nombre}: {temps} temporadas en el {eq.nombre}")
    print("\n")


    # --- EJERCICIO 8: Parejas más Minutos Juntos ---
    print("--- EJERCICIO 8 (PAREJAS MÁS MINUTOS JUNTOS) ---")
    top_parejas = la_liga.obtener_parejas_mas_minutos_juntos(10)
    for j1, j2, eq, minutos in top_parejas:
        print(f"- {j1.nombre} & {j2.nombre} | {eq.nombre} | Minutos: {minutos}")
    print("\n")


    # --- EJERCICIO 9: Jugadores Enteros (Filtro N'Kono) ---
    print("--- EJERCICIO 9 (JUGADORES ENTEROS) ---")
    resultados_integros = la_liga.obtener_top_jugadores_íntegros(3)
    for nombre, partidos in resultados_integros:
        print(f"- {nombre}: {partidos} partidos enteros jugados.")
    print("\n")


    # --- EJERCICIO 10: Tarjetas por Equipo y Temporada ---
    print("--- EJERCICIO 10 (TARJETAS POR EQUIPO) ---")
    busquedas_ej10 = [
        ("R.C.D. Espanyol", "2012-13"),
        ("Real Zaragoza CD", "1996-97"),
        ("Real Zaragoza CD", "1995-96")
    ]
    for equipo, temporada in busquedas_ej10:
        tarjetas = la_liga.obtener_tarjetas_equipo_temporada(equipo, temporada)
        print(f"- {equipo} ({temporada}): {tarjetas} tarjetas conjuntas.")
    print("\n")


    # --- EJERCICIO 11: Revulsivos de Oro ---
    print("--- EJERCICIO 11 (REVULSIVOS DE ORO) ---")
    nombres_ej11 = ["MORATA", "LOINAZ", "BOJAN"]
    resultados_ej11 = la_liga.obtener_revulsivos(nombres_ej11)
    for nombre in nombres_ej11:
        if nombre in resultados_ej11:
            goles, min_por_gol = resultados_ej11[nombre]
            print(f"- {nombre}: {goles} goles. Marca un gol cada {min_por_gol} minutos.")
    print("\n")


    # --- EJERCICIO 12: Años en Activo ---
    print("--- EJERCICIO 12 (AÑOS EN ACTIVO) ---")
    top_anios = la_liga.obtener_top_jugadores_mas_temporadas(4)
    for nombre, anios, anio_inicio, anio_fin in top_anios:
        print(f"- {nombre}: {anios} años en activo (De {anio_inicio} a {anio_fin}).")
    print("\n")


    # --- EJERCICIO 13: Jugadores Impolutos ---
    print("--- EJERCICIO 13 (JUGADORES IMPOLUTOS) ---")
    resultados_impolutos = la_liga.obtener_top_jugadores_impolutos(3)
    for nombre, partidos in resultados_impolutos:
        print(f"- {nombre}: {partidos} partidos disputados de forma impoluta.")
    print("\n")


    # --- EJERCICIO 14: Más Sustituidos ---
    print("--- EJERCICIO 14 (MÁS SUSTITUIDOS) ---")
    resultados_sustituidos = la_liga.obtener_top_jugadores_sustituidos(3)
    for nombre, cambios in resultados_sustituidos:
        if "ETXEBERRIA" in nombre:
            print(f"- {nombre}: Cambiado en {cambios}")
        else:
            print(f"- {nombre}: Cambiado en {cambios} ocasiones.")
    print("\n")


    # --- EJERCICIO 15: Goleadores de una Sola Temporada ---
    print("--- EJERCICIO 15 (GOLEADORES POR TEMPORADA) ---")
    resultados_unicos = la_liga.obtener_top_goleadores_unicos(4)
    for r in resultados_unicos:
        print(f"- {r['nombre']}: {r['goles']} goles. Todos anotados en la {r['temporada']}.")
    print("\n")


    # --- EJERCICIO 16: Ratio Goleador (Minutos/Gol) ---
    print("--- EJERCICIO 16 (TOP EFICIENCIA GOLEADORA) ---")
    resultados_eficiencia = la_liga.obtener_top_eficiencia_goleadora(10)
    for r in resultados_eficiencia:
        print(f"- {r['nombre']}: {r['goles']} goles. Marca un gol cada {r['ratio']:.1f} minutos.")
    print("\n")


    # --- EJERCICIO 17 (Sequía goleadora / Porteros) ---
    print("--- EJERCICIO 17 (MÁS PARTIDOS SIN MARCAR) ---")
    
    top_n = 3
    resultados_ej17 = la_liga.obtener_top_jugadores_sin_gol(top_n)
    
    for r in resultados_ej17:
        # Formato exacto del boletín: "...partidos enteros sin celebrar un gol."
        print(f"- {r['nombre']}: {r['completos']} partidos enteros sin celebrar un gol.")
            
    print("\n")


# --- EJERCICIO 18 (Goles por décadas - Prioridad Cantidad) ---
    print("--- EJERCICIO 18 (GOLES POR DÉCADAS) ---")
    
    # Solicitamos el top 5 del boletín
    resultados_ej18 = la_liga.obtener_jugadores_goles_decadas_top(5)
    
    for r in resultados_ej18:
        decadas_str = ", ".join(map(str, r['decadas']))
        
        # Formateo manual para coincidir con el recorte del PDF en Unamuno
        nombre_imp = r['nombre']
        if "UNAMUNO" in nombre_imp:
            nombre_imp = "VICT. UNAMUNO"
            
        print(f"- {nombre_imp}: Goles en {r['num_decadas']} décadas distintas ({decadas_str}).")
            
    print("\n")

if __name__ == "__main__":
    main()