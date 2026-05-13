from factoria import FactoriaMetro

def main():
    # --- 1. CARGA Y VALIDACIÓN DE DATOS ---
    archivo_metro = 'líneas y estaciones Metro Madrid.xlsx'
    
    print("=== SISTEMA DE GESTIÓN DE METRO MADRID ===")
    print(f"Iniciando la lectura del archivo: {archivo_metro}")
    
    lineas_originales = FactoriaMetro.leer_excel(archivo_metro)
    print("Lectura y validación completadas.\n")

    

    # --- 2. TRANSFORMACIONES BIDIRECTONALES ---
    print("--- Fase de Transformación de Estructuras ---")
    # De Líneas (Lista ordenada) a Estaciones (Conjunto de transbordos)
    estaciones_generadas = lineas_originales.a_estaciones()
    
    # De Estaciones a Líneas (Recíproco)
    lineas_reconstruidas = estaciones_generadas.a_lineas()

    # Comprobación de Igualdad e Identidad (Requisito del Boletín)
    print(f"¿Son el mismo objeto en memoria? (is): {lineas_originales is lineas_reconstruidas}")
    print(f"¿Contienen la misma información? (==): {lineas_originales == lineas_reconstruidas}")

    # --- 3. CONSULTAS BÁSICAS SOBRE LA RED ---
    print("\n--- Análisis de Estaciones y Líneas ---")
    
    # ... después de las transformaciones ...
    
    print("\n--- Estadísticas de la Red ---")
    total_estaciones = estaciones_generadas.obtener_total_estaciones()
    print(f"La red de Metro analizada tiene un total de {total_estaciones} estaciones únicas.")

    # ... resto del código (consultas, criticidad, etc.) ...

    # Líneas circulares
    print("Líneas circulares detectadas:")
    for nombre, linea in lineas_originales.coleccion.items():
        if linea.es_circular():
            print(f" - {nombre}: Comienza y termina en {linea.paradas[0]}")

    # Estaciones con más transbordos
    top_estaciones, num_lineas = estaciones_generadas.estaciones_con_mas_lineas()
    print(f"\nNodos con más conexiones ({num_lineas} líneas):")
    print(f" - {', '.join(top_estaciones)}")

    # --- 4. ANÁLISIS DE GRAFO Y CONECTIVIDAD ---
    print("\n--- Análisis de Robustez de la Red (Grafos) ---")
    
    conexo_original = estaciones_generadas.es_conexo()
    print(f"¿Es la red actual totalmente conexa?: {'SÍ' if conexo_original else 'NO'}")

    # Análisis de Criticidad: ¿Qué línea es más vital?
    print("\nCalculando impacto por supresión de líneas:")
    linea_mas_critica = ""
    max_aisladas = -1

    for nombre_linea in lineas_originales.coleccion.keys():
        aisladas = estaciones_generadas.contar_estaciones_aisladas(nombre_linea)
        
        # Guardamos la que más daño hace a la red
        if aisladas > max_aisladas:
            max_aisladas = aisladas
            linea_mas_critica = nombre_linea
        
        # Informamos si es una línea prescindible
        if aisladas == 0:
            print(f" ✅ La '{nombre_linea}' es prescindible (No aísla estaciones).")

    print(f"\n🏆 LÍNEA MÁS CRÍTICA: '{linea_mas_critica}'")
    print(f"   Su supresión dejaría {max_aisladas} estaciones sin conexión al núcleo.")

    # --- 5. GEOLOCALIZACIÓN Y DISTANCIAS ---
    print("\n--- Servicios de Geolocalización ---")
    
    DICCIONARIO_COORDENADAS = {
        "Sol": (40.4168, -3.7033), "Callao": (40.4202, -3.7056),
        "Gran Vía": (40.4201, -3.7016), "Tribunal": (40.4260, -3.7003),
        "Plaza de España": (40.4234, -3.7122), "Príncipe Pío": (40.4209, -3.7196),
        "Ópera": (40.4182, -3.7093), "Cuatro Caminos": (40.4485, -3.7041),
        "Nuevos Ministerios": (40.4447, -3.6922), "Avenida de América": (40.4389, -3.6766),
        "Plaza Castilla": (40.4669, -3.6892), "Atocha – Renfe": (40.4065, -3.6895),
        "Estación del Arte": (40.4093, -3.6924), "Legazpi": (40.3914, -3.6950),
        "Laguna": (40.3989, -3.7444), "Embajadores": (40.4042, -3.7020),
        "Diego de León": (40.4347, -3.6750), "Pacífico": (40.4001, -3.6761),
        "Méndez Álvaro": (40.3948, -3.6687), "Alonso Martínez": (40.4275, -3.6959)
    }

    for nombre, lat_lon in DICCIONARIO_COORDENADAS.items():
        if nombre in estaciones_generadas.coleccion:
            estaciones_generadas.coleccion[nombre].asignar_coordenada(*lat_lon)

    # Prueba de cercanía (El Retiro)
    lat_r, lon_r = 40.4153, -3.6845
    cercana, dist = estaciones_generadas.estacion_mas_cercana(lat_r, lon_r)
    print(f"Punto: El Retiro -> Estación más cercana: {cercana.nombre} ({dist:.2f} km)")

    # --- 6. CÁLCULO DE TRAYECTOS (BFS) ---
    print("\n--- Motor de Búsqueda de Rutas (BFS) ---")
    orig, dest = "Sol", "Laguna"
    
    # 6.1 Trayecto Directo
    directas = estaciones_generadas.trayecto_directo(orig, dest)
    if directas:
        print(f"Directo: De {orig} a {dest} vía {directas}")
    else:
        print(f"Directo: No existe conexión sin transbordo entre {orig} y {dest}")

    # 6.2 Trayecto con 1 Transbordo (Lógica manual)
    rutas_1 = estaciones_generadas.trayecto_un_transbordo(orig, dest)
    if rutas_1:
        r = rutas_1[0]
        print(f"Sugerencia 1 transbordo: {orig} -> {r['estacion_cambio']} ({r['linea_1']}) -> {dest} ({r['linea_2']})")

    # 6.3 Ruta Óptima General (Generalización)
    ruta_final = estaciones_generadas.ruta_optima_general(orig, dest)
    if ruta_final:
        print(f"Ruta óptima calculada: {' -> '.join(ruta_final)}")

    print("\n==========================================")
    print("FIN DEL PROCESO")

if __name__ == "__main__":
    main()
