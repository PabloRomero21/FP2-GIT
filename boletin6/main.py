from fabrica_elecciones import FabricaElecciones

def main():
    # 1. Definimos la ruta del archivo Excel (asegúrate de que el nombre sea exacto)
    ruta_archivo = "PROV_02_202307_1.xlsx" 

    print("Iniciando la lectura y construcción de datos... Esto puede tardar unos segundos.")
    
    try:
        # 2. Usamos tu patrón Factory para construir todo el árbol de objetos
        fabrica = FabricaElecciones(ruta_xlsx=ruta_archivo)
        espana = fabrica.construir()
            
        print(f"\n¡Datos cargados con éxito para: {espana.nombre}!\n")

        # 3. Pruebas de los métodos de graficado
        # PRUEBA 1: Nivel Nacional
    #     print(">> Generando gráfica a nivel NACIONAL...")
    #     espana.graficar_resultados(nivel="nacional")

    #     # IMPORTANTE: Los nombres de las comunidades y provincias deben escribirse 
    #     # EXACTAMENTE igual a como vienen en el Excel (mayúsculas, tildes, etc.)
    #     comunidad_prueba = "Andalucía" 
    #     provincia_prueba = "Sevilla"

    #     # PRUEBA 2: Nivel Comunidad Autónoma
    #     print(f">> Generando gráfica a nivel COMUNIDAD ({comunidad_prueba})...")
    #     espana.graficar_resultados(nivel="comunidad", id_comunidad=comunidad_prueba)

    #     # PRUEBA 3: Nivel Provincial
    #     print(f">> Generando gráfica a nivel PROVINCIAL ({provincia_prueba})...")
    #     espana.graficar_resultados(nivel="provincial", id_comunidad=comunidad_prueba, id_provincia=provincia_prueba)




# Obtenemos los datos puros desde la clase Pais
        ccaa_max, provincia_max = espana.ranking_votos_nulos_blancos()

        # Nos encargamos de la presentación aquí en el main
        print("\n--- 🏆 MAYOR PORCENTAJE DE VOTOS NULOS Y EN BLANCO ---")
        print(f"🏢 Comunidad Autónoma: {ccaa_max.nombre} ({ccaa_max.porcentaje_nulos_blancos:.2f}%)")
        print(f"📍 Provincia:          {provincia_max.nombre} ({provincia_max.porcentaje_nulos_blancos:.2f}%)")
        print("----------------------------------------------------\n")


        # --- 3. SECCIÓN DE PARTICIPACIÓN CERA ---
        ccaa_cera, provincia_cera = espana.ranking_participacion_cera()

        print("--- 🌍 MAYOR PARTICIPACIÓN DE VOTANTES CERA (Extranjero) ---")
        print(f"🏢 Comunidad Autónoma: {ccaa_cera.nombre} ({ccaa_cera.participacion_cera:.2f}%)")
        print(f"📍 Provincia:          {provincia_cera.nombre} ({provincia_cera.participacion_cera:.2f}%)")
        print("----------------------------------------------------------\n")

# --- 4. SECCIÓN: PARTIDOS POR NÚMERO DE PROVINCIAS ---
        # Prueba 1: Partidos en las 52 provincias (Nacionales)
        n_prov_nacional = 52
        partidos_52 = espana.partidos_en_n_provincias(n_prov_nacional)
        
        print(f"--- 🏛️ PARTIDOS PRESENTADOS EN {n_prov_nacional} PROVINCIAS ---")
        if partidos_52:
            for p in partidos_52:
                print(f" - {p.nombre}")
        else:
            print("Ningún partido cumple esta condición.")
            
        print("\n")

        # Prueba 2: Partidos en exactamente 1 provincia (Locales/Regionalistas)
        n_prov_local = 1
        partidos_1 = espana.partidos_en_n_provincias(n_prov_local)
        
        print(f"--- 📍 PARTIDOS PRESENTADOS EN {n_prov_local} SOLA PROVINCIA ---")
        if partidos_1:
            for p in partidos_1:
                print(f" - {p.nombre}")
        else:
            print("Ningún partido cumple esta condición.")
        print("----------------------------------------------------------\n")


        # --- 5. SECCIÓN: PROPORCIÓN CERA VS POBLACIÓN ---
        ccaa_prop_cera = espana.ccaa_mayor_proporcion_cera()
        
        print("--- 📊 MAYOR PROPORCIÓN DE VOTANTES CERA VS POBLACIÓN ---")
        print(f"🏢 Comunidad Autónoma: {ccaa_prop_cera.nombre}")
        print(f"📈 Proporción:         {ccaa_prop_cera.proporcion_votantes_cera_poblacion:.4f}% de su población total")
        print("---------------------------------------------------------\n")


        # --- 6. SECCIÓN: LEY D'HONDT ---
        comunidad_dhondt = "Comunidad de Madrid"
        provincia_dhondt = "Madrid"
        
        resultados, escanos_totales = espana.calcular_escanos_dhondt(comunidad_dhondt, provincia_dhondt)
        
        print(f"--- ⚖️ REPARTO D'HONDT EN: {provincia_dhondt.upper()} ---")
        print(f"Total de escaños a repartir: {escanos_totales}")
        print("------------------------------------------")
        
        for partido, escanos in resultados.items():
            print(f" 🏛️ {escanos} escaños -> {partido}")
        print("------------------------------------------\n")




    except FileNotFoundError:
         print(f"\n[ERROR] No se ha encontrado el archivo '{ruta_archivo}'.")
         print("Asegúrate de que el archivo Excel está en la misma carpeta que main.py.")
    except Exception as e:
         print(f"\n[ERROR] Ocurrió un fallo inesperado: {e}")

# Este bloque asegura que main() solo se ejecute si corremos este archivo directamente,
# y no si importamos main.py desde otro lugar. Es una buena práctica en Python.
if __name__ == "__main__":
    main()