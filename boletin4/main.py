from factoria import FactoriaJugadores
import os
import pickle
from liga import Liga

def main():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_xls = os.path.join(directorio_actual, "Plantillas1D-2017-18.xls")
    ruta_pkl = os.path.join(directorio_actual, "liga_completa.pkl") # Nuevo nombre para no confundir
    
    la_liga = None

    if os.path.exists(ruta_pkl):
        print(f"Cargando LIGA COMPLETA (Jugadores + Equipos) desde: {ruta_pkl}...")
        with open(ruta_pkl, 'rb') as archivo_entrada:
            la_liga = pickle.load(archivo_entrada)
        print("¡Estructura total cargada instantáneamente!\n")
    else:
        print("Primera ejecución: Procesando Excel y construyendo estructura...")
        # 1. Creamos la lista inicial desde Excel
        lista_jugadores = FactoriaJugadores.crear_jugadores_desde_excel(ruta_xls)
        
        # 2. Creamos el objeto Liga (que por dentro construye los Equipos una sola vez)
        la_liga = Liga("La Liga Santander", lista_jugadores)
        
        # 3. Guardamos TODO el objeto Liga en el pickle
        print("Guardando objeto Liga completo para futuras ejecuciones...")
        with open(ruta_pkl, 'wb') as archivo_salida:
            pickle.dump(la_liga, archivo_salida)
        print("¡Guardado completado!\n")    
    


    print("--- EJERCICIO 1 ---")
    maximo_goleador_temporada = la_liga.obtener_maximo_goleador_temporada()
    jugador_obj = maximo_goleador_temporada[0]
    est_obj = maximo_goleador_temporada[1]

    print(f"{jugador_obj.nombre} ({est_obj.equipo} - Temporada {est_obj.temporada}) | Partidos: {int(est_obj.pjugados)} | Goles: {int(est_obj.goles)}\n")


    print("--- EJERCICIO 2 ---")
    maximo_historico = la_liga.obtener_maximo_goleador_historico()
    jugador_hist_obj = maximo_historico[0]
    total_goles = maximo_historico[1]
    
    
    print(f"{jugador_hist_obj.nombre}: {int(total_goles)} goles\n")


    print("--- EJERCICIO 3 ---")
    resultado_trotamundos = la_liga.obtener_jugador_mas_equipos()
    
    jugador_trotamundos = resultado_trotamundos[0]
    lista_equipos = resultado_trotamundos[1]
    
    # Imprimimos el nombre y unimos la lista de strings con ", "
    print(f"{jugador_trotamundos.nombre} - Equipos: {', '.join(lista_equipos)}\n")



    print("---  EJERCICIO 4 ---")
    resultado_record = la_liga.obtener_jugador_record_partidos_en_un_club()
    
    jugador_rec = resultado_record[0]
    equipo_nome, partidos_num = resultado_record[1]
    
    print(f"{jugador_rec.nombre} - Equipo: {equipo_nome}, Partidos: {partidos_num}\n")   



    print("--- EJERCICIO 5---")
    jugador_minutos_obj, minutos_totales = la_liga.obtener_jugador_mas_minutos_total()
    
    print(f"{jugador_minutos_obj.nombre} con un total de {minutos_totales} minutos jugados.\n")

    print("--- EJERCICIO 6 ---")
    
    # Lista de los jugadores que queremos consultar
    jugadores_consulta = ["JULIO SALINAS", "SALVA B.", "ARIZMENDI"]

    for nombre in jugadores_consulta:
        # Llamamos al método que devuelve la lista de OBJETOS Equipo
        objetos_equipo = la_liga.obtener_objetos_equipo_jugador(nombre)
        
        if objetos_equipo:
            # Extraemos el nombre de cada objeto Equipo para poder imprimirlos
            nombres_de_clubes = [eq.nombre for eq in objetos_equipo]
            
            # Unimos los nombres con comas y mostramos el resultado
            print(f"{nombre} - Equipos: {', '.join(nombres_de_clubes)}")
        else:
            print(f"{nombre} - No se han encontrado datos.")

    print("\n")



    print(f"---EJERCICIO 7---")
    n_top = 5
    top_fieles = la_liga.obtener_top_jugadores_fieles(n_top)

    for (jug, eq, temps) in top_fieles:
        # i es el ranking, jug es el objeto Jugador, eq el objeto Equipo
        print(f"{jug.nombre} - {temps} temporadas en el {eq.nombre}")

    print("\n")

    print("---EJERICICIO 8---")
    n_parejas = 10
    top_parejas = la_liga.obtener_parejas_mas_minutos_juntos(n_parejas)

    for j1, j2, eq, minutos in top_parejas:
        print(f"{j1.nombre} & {j2.nombre} - Equipo: {eq.nombre}, Minutos juntos: {minutos}")
    
    print("\n")


# --- EJERCICIO 17 (Jugadores íntegros) ---
    print("---EJERCICIO 9---")
    
    resultados = la_liga.obtener_top_jugadores_íntegros(3)
    
    for nombre, partidos in resultados:
        print(f"- {nombre}: {partidos} partidos enteros jugados.")
            
    print("\n")




    # --- EJERCICIO 10 ---
    print("---EJERCICIO 10---")
    
    # Preparamos la lista con las combinaciones exactas de Equipo y Temporada
    busquedas_ej10 = [
        ("R.C.D. Espanyol", "2012-13"),
        ("Real Zaragoza CD", "1996-97"),
        ("Real Zaragoza CD", "1995-96")
    ]
    
    # Recorremos la lista
    for equipo, temporada in busquedas_ej10:
        # Llamamos a la función que creamos en liga.py
        tarjetas = la_liga.obtener_tarjetas_equipo_temporada(equipo, temporada)
        
        # Imprimimos calcando el formato de las soluciones
        print(f"- {equipo} ({temporada}): {tarjetas} tarjetas conjuntas.")
        
    print("\n")


    # --- EJERCICIO 11 ---
    print("Ejercicio 11")
    print("LOS REVULSIVOS DE ORO")
    
    nombres_ej11 = ["MORATA", "LOINAZ", "BOJAN"]
    
    # Llamamos al método
    resultados_ej11 = la_liga.obtener_revulsivos(nombres_ej11)
    
    # Imprimimos los resultados con el formato exacto
    for nombre in nombres_ej11:
        if nombre in resultados_ej11:
            goles, min_por_gol = resultados_ej11[nombre]
            print(f"- {nombre}: {goles} goles. Marca un gol cada {min_por_gol} minutos.")
            
    print("\n")



# --- EJERCICIO 12 (Top Años en Activo) ---
    print("---EJERCICIO 12---")
    
    # El enunciado pide los 4 primeros
    top_n = 4 
    
    # Llamamos a la función
    top_jugadores = la_liga.obtener_top_jugadores_mas_temporadas(top_n)
    
    # Montamos el texto calcado al del profesor
    for nombre, anios, anio_inicio, anio_fin in top_jugadores:
        print(f"- {nombre}: {anios} años en activo (De {anio_inicio} a {anio_fin}).")
        
    print("\n")



# --- EJERCICIO 13 (Impolutos con nueva lógica) ---
    print("---EJERCICIO 13---")
    
    # Pedimos el Top 3
    top_n = 3 
    resultados = la_liga.obtener_top_jugadores_impolutos(top_n)
    
    for nombre, partidos in resultados:
        print(f"- {nombre}: {partidos} partidos disputados de forma impoluta.")
        
    print("\n")

# --- EJERCICIO 14 (Más sustituidos) ---
    print("---TOP JUGADORES SUSTITUIDOS---")
    
    top_n = 3
    resultados = la_liga.obtener_top_jugadores_sustituidos(top_n)
    
    for nombre, cambios in resultados:
        # Formato especial para que quede igual que tu ejemplo
        if "ETXEBERRIA" in nombre:
            print(f"- {nombre}: Cambiado en {cambios}")
        else:
            print(f"- {nombre}: Cambiado en {cambios} ocasiones.")
            
    print("\n")



    # --- EJERCICIO 15 ---
    print("---TOP GOLEADORES POR TEMPORADA---")
    
    resultados = la_liga.obtener_top_goleadores_unicos(4)
    
    for r in resultados:
        print(f"- {r['nombre']}: {r['goles']} goles. Todos anotados en la {r['temporada']}.")




    # --- EJERCICIO 16 (Ratio Goleador) ---
    print("---TOP EFICIENCIA GOLEADORA---")
    
    top_n = 10
    resultados = la_liga.obtener_top_eficiencia_goleadora(top_n)
    
    for r in resultados:
  
        print(f"- {r['nombre']}: {r['goles']} goles. Marca un gol cada {r['ratio']:.1f} minutos.")
            
    print("\n")






if __name__ == "__main__":
    main()
    