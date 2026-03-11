import os
import pickle
from factoria import FactoriaJugadores
from liga import Liga

def main():
    # =========================================================================
    # --- CONFIGURACIÓN DE RUTAS Y CARGA DE DATOS ---
    # =========================================================================
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


    # =========================================================================
    # --- EJECUCIÓN DE EJERCICIOS ---
    # =========================================================================

    # --- EJERCICIO 1 (MÁXIMO GOLEADOR TEMPORADA) ---
    print("--- EJERCICIO 1 (MÁXIMO GOLEADOR TEMPORADA) ---")
    maximo_goleador_temporada = la_liga.obtener_maximo_goleador_temporada()
    jugador_obj = maximo_goleador_temporada[0]
    est_obj = maximo_goleador_temporada[1]
    print(f"- {jugador_obj.nombre} ({est_obj.equipo} - Temporada {est_obj.temporada}) | Partidos: {int(est_obj.pjugados)} | Goles: {int(est_obj.goles)}")
    print("\n")


    # --- EJERCICIO 2 (MÁXIMO GOLEADOR HISTÓRICO) ---
    print("--- EJERCICIO 2 (MÁXIMO GOLEADOR HISTÓRICO) ---")
    maximo_historico = la_liga.obtener_maximo_goleador_historico()
    jugador_hist_obj = maximo_historico[0]
    total_goles = maximo_historico[1]
    print(f"- {jugador_hist_obj.nombre}: {int(total_goles)} goles totales.")
    print("\n")


    # --- EJERCICIO 3 (JUGADOR TROTAMUNDOS) ---
    print("--- EJERCICIO 3 (JUGADOR TROTAMUNDOS) ---")
    resultado_trotamundos = la_liga.obtener_jugador_mas_equipos()
    jugador_trotamundos = resultado_trotamundos[0]
    lista_equipos = resultado_trotamundos[1]
    print(f"- {jugador_trotamundos.nombre} - Equipos: {', '.join(lista_equipos)}")
    print("\n")


    # --- EJERCICIO 4 (RÉCORD PARTIDOS EN UN CLUB) ---
    print("--- EJERCICIO 4 (RÉCORD PARTIDOS EN UN CLUB) ---")
    resultado_record = la_liga.obtener_jugador_record_partidos_en_un_club()
    jugador_rec = resultado_record[0]
    equipo_nome, partidos_num = resultado_record[1]
    print(f"- {jugador_rec.nombre} - Equipo: {equipo_nome}, Partidos: {partidos_num}")   
    print("\n")


    # --- EJERCICIO 5 (MÁXIMOS MINUTOS JUGADOS) ---
    print("--- EJERCICIO 5 (MÁXIMOS MINUTOS JUGADOS) ---")
    jugador_minutos_obj, minutos_totales = la_liga.obtener_jugador_mas_minutos_total()
    print(f"- {jugador_minutos_obj.nombre} con un total de {minutos_totales} minutos jugados.")
    print("\n")


    # --- EJERCICIO 6 (CONSULTA DE CLUBES POR JUGADOR) ---
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


    # --- EJERCICIO 7 (TOP JUGADORES FIELES) ---
    print("--- EJERCICIO 7 (TOP JUGADORES FIELES) ---")
    top_fieles = la_liga.obtener_top_jugadores_fieles(5)
    for (jug, eq, temps) in top_fieles:
        print(f"- {jug.nombre}: {temps} temporadas en el {eq.nombre}")
    print("\n")


    # --- EJERCICIO 8 (PAREJAS MÁS MINUTOS JUNTOS) ---
    print("--- EJERCICIO 8 (PAREJAS MÁS MINUTOS JUNTOS) ---")
    top_parejas = la_liga.obtener_parejas_mas_minutos_juntos(10)
    for j1, j2, eq, minutos in top_parejas:
        print(f"- {j1.nombre} & {j2.nombre} | {eq.nombre} | Minutos: {minutos}")
    print("\n")


    # --- EJERCICIO 9 (JUGADORES ENTEROS) ---
    print("--- EJERCICIO 9 (JUGADORES ENTEROS) ---")
    resultados_integros = la_liga.obtener_top_jugadores_íntegros(3)
    for nombre, partidos in resultados_integros:
        print(f"- {nombre}: {partidos} partidos enteros jugados.")
    print("\n")


    # --- EJERCICIO 10 (TARJETAS POR EQUIPO Y TEMPORADA) ---
    print("--- EJERCICIO 10 (TARJETAS POR EQUIPO Y TEMPORADA) ---")
    busquedas_ej10 = [
        ("R.C.D. Espanyol", "2012-13"),
        ("Real Zaragoza CD", "1996-97"),
        ("Real Zaragoza CD", "1995-96")
    ]
    for equipo, temporada in busquedas_ej10:
        tarjetas = la_liga.obtener_tarjetas_equipo_temporada(equipo, temporada)
        print(f"- {equipo} ({temporada}): {tarjetas} tarjetas conjuntas.")
    print("\n")


    # --- EJERCICIO 11 (REVULSIVOS DE ORO) ---
    print("--- EJERCICIO 11 (REVULSIVOS DE ORO) ---")
    nombres_ej11 = ["MORATA", "LOINAZ", "BOJAN"]
    resultados_ej11 = la_liga.obtener_revulsivos(nombres_ej11)
    for nombre in nombres_ej11:
        if nombre in resultados_ej11:
            goles, min_por_gol = resultados_ej11[nombre]
            print(f"- {nombre}: {goles} goles. Marca un gol cada {min_por_gol} minutos.")
    print("\n")


    # --- EJERCICIO 12 (AÑOS EN ACTIVO) ---
    print("--- EJERCICIO 12 (AÑOS EN ACTIVO) ---")
    top_anios = la_liga.obtener_top_jugadores_mas_temporadas(4)
    for nombre, anios, anio_inicio, anio_fin in top_anios:
        print(f"- {nombre}: {anios} años en activo (De {anio_inicio} a {anio_fin}).")
    print("\n")


    # --- EJERCICIO 13 (JUGADORES IMPOLUTOS) ---
    print("--- EJERCICIO 13 (JUGADORES IMPOLUTOS) ---")
    resultados_impolutos = la_liga.obtener_top_jugadores_impolutos(3)
    for nombre, partidos in resultados_impolutos:
        print(f"- {nombre}: {partidos} partidos disputados de forma impoluta.")
    print("\n")


    # --- EJERCICIO 14 (MÁS SUSTITUIDOS) ---
    print("--- EJERCICIO 14 (MÁS SUSTITUIDOS) ---")
    resultados_sustituidos = la_liga.obtener_top_jugadores_sustituidos(3)
    for nombre, cambios in resultados_sustituidos:
        if "ETXEBERRIA" in nombre:
            print(f"- {nombre}: Cambiado en {cambios}")
        else:
            print(f"- {nombre}: Cambiado en {cambios} ocasiones.")
    print("\n")


    # --- EJERCICIO 15 (GOLEADORES DE UNA SOLA TEMPORADA) ---
    print("--- EJERCICIO 15 (GOLEADORES POR TEMPORADA) ---")
    resultados_unicos = la_liga.obtener_top_goleadores_unicos(4)
    for r in resultados_unicos:
        print(f"- {r['nombre']}: {r['goles']} goles. Todos anotados en la {r['temporada']}.")
    print("\n")


    # --- EJERCICIO 16 (TOP EFICIENCIA GOLEADORA) ---
    print("--- EJERCICIO 16 (TOP EFICIENCIA GOLEADORA) ---")
    resultados_eficiencia = la_liga.obtener_top_eficiencia_goleadora(10)
    for r in resultados_eficiencia:
        print(f"- {r['nombre']}: {r['goles']} goles. Marca un gol cada {r['ratio']:.1f} minutos.")
    print("\n")


    # --- EJERCICIO 17 (MÁS PARTIDOS SIN MARCAR) ---
    print("--- EJERCICIO 17 (MÁS PARTIDOS SIN MARCAR) ---")
    top_n = 3
    resultados_ej17 = la_liga.obtener_top_jugadores_sin_gol(top_n)
    for r in resultados_ej17:
        print(f"- {r['nombre']}: {r['completos']} partidos enteros sin celebrar un gol.")
    print("\n")


    # --- EJERCICIO 18 (GOLES POR DÉCADAS) ---
    print("--- EJERCICIO 18 (GOLES POR DÉCADAS) ---")
    lista_nombres = []
    resultados_ej18 = la_liga.obtener_jugadores_goles_decadas_exacto(5)
    for r in resultados_ej18:
        decadas_str = ", ".join(map(str, r['decadas']))
        nombre_final = r['nombre']
        if "UNAMUNO" in nombre_final: nombre_final = "VICT. UNAMUNO"
        if "BIENZOBAS" in nombre_final: nombre_final = "P. BIENZOBAS"
        print(f"- {nombre_final}: Goles en {r['num_decadas']} décadas distintas ({decadas_str}).")
        lista_nombres.append(nombre_final)
    print("\n")


    # --- EJERCICIO 19 (DESCENSOS POR TEMPORADA) ---
    print("--- EJERCICIO 19 (DESCENSOS POR TEMPORADA) ---")
    temporadas_consulta = ["1950-51", "1953-54", "1955-56", "1961-62", "1962-63", "1964-65", "1988-89", "1996-97", "1998-99"]
    for temp in temporadas_consulta:
        descendidos = la_liga.obtener_descendidos(temp)
        if descendidos:
            lista_str = ", ".join(descendidos)
            print(f"- Temporada {temp}: Descendieron {len(descendidos)} equipos: {lista_str}")
    print("\n")


    # --- EJERCICIO 20 (TOP EQUIPOS CON MÁS DESCENSOS) ---
    print("--- EJERCICIO 20 (TOP EQUIPOS CON MÁS DESCENSOS) ---")
    # Asumiendo que este método sigue devolviendo un string con formato como indicaba tu comentario original
    resultado_descensos = la_liga.obtener_equipos_mas_descendidos(3)
    print(resultado_descensos)
    print("\n")


    # --- EJERCICIO 21 (EQUIPOS ASCENDIDOS POR TEMPORADA) ---
    print("--- EJERCICIO 21 (EQUIPOS ASCENDIDOS POR TEMPORADA) ---")
    temporadas_ascensos = [
        "1941-42", "1950-51", "1951-52", "1954-55", 
        "1956-57", "1962-63", "1963-64", "1965-66", 
        "1971-72", "1989-90", "1999-00"
    ]
    for temp in temporadas_ascensos:
        ascendidos = la_liga.obtener_ascendidos(temp)
        if ascendidos:
            equipos_str = ", ".join(ascendidos)
            print(f"- Temporada {temp}: Ascendieron {len(ascendidos)} equipos: {equipos_str}")
    print("\n")


    # --- EJERCICIO 22 (EQUIPOS MÁS ASCENDIDOS) ---
    print("--- EJERCICIO 22 (EQUIPOS MÁS ASCENDIDOS) ---")
    top_ascensos = 1
    resultados_ascensos = la_liga.obtener_equipos_mas_ascendidos(top_ascensos)
    for equipo, num_ascensos in resultados_ascensos:
        print(f"- {equipo}: {num_ascensos} ascensos")
    print("\n")


    # --- EJERCICIO 23 (EQUIPOS CON MÁS TEMPORADAS) ---
    print("--- EJERCICIO 23 (EQUIPOS CON MÁS TEMPORADAS) ---")
    top_n = 10
    resultados_temporadas = la_liga.obtener_equipos_mas_temporadas(top_n)
    for equipo, num in resultados_temporadas:
        print(f"- {equipo}: {num} temporadas")
    print("\n")


    # --- EJERCICIO 24 (EQUIPOS CON MENOS TEMPORADAS) ---
    print("--- EJERCICIO 24 (EQUIPOS CON MENOS TEMPORADAS) ---")
    top_n_menos = 5 
    resultados_menos_temporadas = la_liga.obtener_equipos_menos_temporadas(top_n_menos)
    for equipo, num in resultados_menos_temporadas:
        print(f"- {equipo}: {num} temporadas")
    print("\n")


    # --- EJERCICIO 25 (EQUIPOS CON MÁS GOLES) ---
    print("--- EJERCICIO 25 (EQUIPOS CON MÁS GOLES) ---")
    top_n_goles = 5 
    resultados_goles = la_liga.obtener_equipos_mas_goles(top_n_goles)
    for equipo, goles in resultados_goles:
        print(f"- {equipo}: {goles} goles")
    print("\n")


    # --- EJERCICIO 26 (EQUIPOS CON MENOS GOLES) ---
    print("--- EJERCICIO 26 (EQUIPOS CON MENOS GOLES) ---")
    top_n_menos_goles = 10 
    resultados_menos_goles = la_liga.obtener_equipos_menos_goles(top_n_menos_goles)
    for equipo, goles in resultados_menos_goles:
        print(f"- {equipo}: {goles} goles")
    print("\n")


    # --- EJERCICIO 27 (MEJORES TEMPORADAS POR RATIO DE GOLES) ---
    print("--- EJERCICIO 27 (MEJORES TEMPORADAS POR RATIO DE GOLES) ---")
    top_n_ratio = 5 
    resultados_ratio = la_liga.obtener_mejores_temporadas_ratio_goles(top_n_ratio)
    for r in resultados_ratio:
        print(f"- Temporada {r['temporada']}: {r['goles']} goles en {r['partidos']} partidos. Media: {r['ratio']:.2f} goles/partido.")
    print("\n")


    # --- EJERCICIO 28 (EMPATES: EQUIPOS MÁS GOLEADORES POR TEMPORADA) ---
    print("--- EJERCICIO 28 (EMPATES: EQUIPOS MÁS GOLEADORES POR TEMPORADA) ---")
    resultados_empates = la_liga.obtener_empates_equipos_mas_goles()
    for empate in resultados_empates:
        equipos_str = ", ".join(empate['equipos'])
        print(f"- Temporada {empate['temporada']}: Máximo goleador fue {equipos_str}")
    print("\n")


    # --- EJERCICIO 29 (RACHAS COMO EQUIPO MÁS GOLEADOR) ---
    print("--- EJERCICIO 29 (RACHAS COMO EQUIPO MÁS GOLEADOR) ---")
    top_n_rachas = 5 
    resultados_rachas = la_liga.obtener_rachas_maximo_goleador(top_n_rachas)
    for equipo, racha in resultados_rachas:
        print(f"- {equipo}: Racha de {racha} temporadas consecutivas siendo el máximo goleador.")
    print("\n")


    # --- EJERCICIO 30 (JUGADORES EN COMÚN ENTRE EQUIPOS) ---
    print("--- EJERCICIO 30 (JUGADORES EN COMÚN ENTRE EQUIPOS) ---")
    equipo_a = "Sevilla F.C."
    equipo_b = "Real Betis B. S."
    comunes = la_liga.obtener_jugadores_comunes(equipo_a, equipo_b)
    if comunes:
        ejemplos_str = ", ".join(comunes[:5])
        print(f"- {equipo_a} vs {equipo_b}: {len(comunes)} jugadores. Ejemplos: {ejemplos_str}")
    print("\n")


    # --- EJERCICIO 31 (MENOR PROMEDIO DE MINUTOS) ---
    print("--- EJERCICIO 31 (MENOR PROMEDIO DE MINUTOS) ---")
    resultados_ej31 = la_liga.obtener_menor_promedio_minutos(5)
    for r in resultados_ej31:
        print(f"- {r['nombre']}: Promedio de {r['promedio']:.1f} minutos por temporada (Total: {r['total_minutos']} minutos en {r['temporadas']} temporadas).")
    print("\n")


    # --- EJERCICIO 32 (MÁS AÑOS FUERA DEL MISMO EQUIPO) ---
    print("--- EJERCICIO 32 (MÁS AÑOS FUERA DEL MISMO EQUIPO) ---")
    resultados_ej32 = la_liga.obtener_top_anios_fuera(5)
    for r in resultados_ej32:
        print(f"- {r['nombre']} - Equipo: {r['equipo']}, Años fuera: {r['anios_fuera']}.")
    print("\n")


    # --- EJERCICIO 33---
    print("Ejercicio 33")
    
    # Obtenemos los 3 mejores (o los que necesites)
    resultados_33 = la_liga.obtener_rachas_sin_tarjetas_desempate_goles(3)
    
    for r in resultados_33:
        # Formato: - NOMBRE: Racha de X temporadas consecutivas.
        print(f"- {r['nombre'].upper()}: Racha de {int(r['racha'])} temporadas consecutivas.")
            
    print("\n")


# --- EJERCICIO 35 (HISTORIAL EN FILAS: ITURRINO) ---
    print("--- EJERCICIO 35 (HISTORIAL COMPLETO EN FILAS) ---")
    
    nombres = ["SARO","MARIN","CHOLIN","P. BIENZOBAS","VICT. UNAMUNO"]
    for nombre_objetivo in lista_nombres:
        historial = la_liga.obtener_historial_jugador_completo(nombre_objetivo)
        print(nombre_objetivo)
        if historial:
            # 1. Obtener los nombres de todas las columnas (las llaves del primer diccionario)
            columnas = list(historial[0].keys())
            
            # 2. Imprimir la cabecera (usamos ljust para dar un ancho fijo de 12 espacios a cada columna)
            cabecera = "".join(col.upper().ljust(12) for col in columnas)
            print(cabecera)
            print("-" * len(cabecera))
            
            # 3. Imprimir cada fila de datos
            for fila in historial:
                linea = ""
                for col in columnas:
                    valor = str(fila.get(col, "-"))
                    linea += valor.ljust(12)
                print(linea)
        else:
            print(f"SISTEMA: No hay datos para {nombre_objetivo}")
                
        print("\n")

if __name__ == "__main__":
    main()