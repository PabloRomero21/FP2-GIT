from fabrica_elecciones import FabricaElecciones


def main():
    ruta_archivo = "C:/Users/romer/Desktop/FP2-GIT/FP2-GIT/boletin6/PROV_02_202307_1.xlsx"

    print("Iniciando la lectura y construccion de datos... Esto puede tardar unos segundos.")

    try:
        fabrica = FabricaElecciones(ruta_xlsx=ruta_archivo)
        espana = fabrica.construir()

        print(f"\nDatos cargados con exito para: {espana.nombre}\n")

        # --- 1. GRAFICAS DE RESULTADOS ---
        espana.graficar_resultados(nivel="nacional")
        espana.graficar_resultados(nivel="comunidad", id_comunidad="Andalucía")
        espana.graficar_resultados(nivel="provincial", id_comunidad="Andalucía", id_provincia="Sevilla")


        # --- 2. RANKING DE VOTOS NULOS Y EN BLANCO ---
        ccaa_max, provincia_max = espana.ranking_votos_nulos_blancos()

        print("--- MAYOR PORCENTAJE DE VOTOS NULOS Y EN BLANCO ---")
        print(f"Comunidad Autonoma : {ccaa_max.nombre} ({ccaa_max.porcentaje_nulos_blancos:.2f}%)")
        print(f"Provincia          : {provincia_max.nombre} ({provincia_max.porcentaje_nulos_blancos:.2f}%)")
        print("----------------------------------------------------\n")


        # --- 3. PARTICIPACION CERA ---
        ccaa_cera, provincia_cera = espana.ranking_participacion_cera()

        print("--- MAYOR PARTICIPACION DE VOTANTES CERA (Extranjero) ---")
        print(f"Comunidad Autonoma : {ccaa_cera.nombre} ({ccaa_cera.participacion_cera:.2f}%)")
        print(f"Provincia          : {provincia_cera.nombre} ({provincia_cera.participacion_cera:.2f}%)")
        print("----------------------------------------------------------\n")


        # --- 4. PARTIDOS POR NUMERO DE PROVINCIAS ---
        n_prov_nacional = 52
        partidos_52 = espana.partidos_en_n_provincias(n_prov_nacional)

        print(f"--- PARTIDOS PRESENTADOS EN {n_prov_nacional} PROVINCIAS ---")
        if partidos_52:
            for p in partidos_52:
                print(f"  - {p.nombre}")
        else:
            print("Ningun partido cumple esta condicion.")
        print()

        n_prov_local = 1
        partidos_1 = espana.partidos_en_n_provincias(n_prov_local)

        print(f"--- PARTIDOS PRESENTADOS EN {n_prov_local} SOLA PROVINCIA ---")
        if partidos_1:
            for p in partidos_1:
                print(f"  - {p.nombre}")
        else:
            print("Ningun partido cumple esta condicion.")
        print("----------------------------------------------------------\n")


        # --- 5. PROPORCION CERA VS POBLACION ---
        ccaa_prop_cera = espana.ccaa_mayor_proporcion_cera()

        print("--- MAYOR PROPORCION DE VOTANTES CERA VS POBLACION ---")
        print(f"Comunidad Autonoma : {ccaa_prop_cera.nombre}")
        print(f"Proporcion         : {ccaa_prop_cera.proporcion_votantes_cera_poblacion:.4f}% de su poblacion total")
        print("---------------------------------------------------------\n")


        # --- 6. LEY D'HONDT ---
        comunidad_dhondt = "Comunidad de Madrid"
        provincia_dhondt = "Madrid"

        resultados, escanos_totales = espana.calcular_escanos_dhondt(comunidad_dhondt, provincia_dhondt)

        print(f"--- REPARTO D'HONDT EN: {provincia_dhondt.upper()} ---")
        print(f"Total de escanos a repartir: {escanos_totales}")
        print("------------------------------------------")
        for partido, escanos in resultados.items():
            print(f"  {escanos} escanos -> {partido}")
        print("------------------------------------------\n")


        # --- 7. AUDITORIA DE ESCANOS ---
        print("--- AUDITORIA DE ESCANOS (EXCEL VS D'HONDT) ---")
        totales, correctas, errores = espana.comprobar_escanos_excel()

        print(f"Provincias analizadas          : {totales}")
        print(f"Provincias con reparto exacto  : {correctas}")
        print(f"Provincias con discrepancias   : {len(errores)}")
        print("------------------------------------------------------------\n")

        if errores:
            print("DETALLE DE LAS DISCREPANCIAS (Mostrando las 3 primeras):")
            for error in errores[:3]:
                print(f"\n  {error['provincia'].upper()} ({error['comunidad']}):")
                print(f"    - Reales (Excel) : {error['reales']}")
                print(f"    - Calculados     : {error['calculados']}")
            if len(errores) > 3:
                print(f"\n  ... y {len(errores) - 3} provincias mas con diferencias.")


        # --- 8. GRAFICAS DE ESCANOS ---
        print("\nGenerando graficas de escanos...")
        print("(Cierra la ventana actual para que aparezca la siguiente)")

        espana.graficar_escanos(nivel="provincial", id_comunidad="Castilla y León", id_provincia="Soria")
        espana.graficar_escanos(nivel="comunidad", id_comunidad="Andalucía")
        espana.graficar_escanos()


        # --- 9. ANALISIS DEL ULTIMO ESCANO ---
        print("\n" + "=" * 60)
        print("LAS BATALLAS MAS AJUSTADAS POR EL ULTIMO ESCANO")
        print("=" * 60)

        analisis_escanos = espana.analizar_ultimo_escano()

        print("TOP 5 PROVINCIAS CON EL MARGEN MAS ESTRECHO:")
        for i, dato in enumerate(analisis_escanos[:5]):
            print(f"\n  {i+1}. {dato['provincia'].upper()} ({dato['comunidad']})")
            print(f"     Ultimo escano         : {dato['ganador']}")
            print(f"     Se quedo a las puertas: {dato['perdedor']}")
            print(f"     Votos faltantes       : {dato['votos_faltantes']}")
        print("=" * 60 + "\n")


        # --- 10. COSTE DEL ESCANO (MAS BARATOS) ---
        print("\n" + "=" * 60)
        print("EL PRECIO DEL ESCANO (LOS MAS BARATOS)")
        print("=" * 60)

        ranking_nac, ranking_prov = espana.coste_del_escano()

        print("\nA NIVEL NACIONAL (Top 5 partidos con escanos mas baratos):")
        for i, dato in enumerate(ranking_nac[:5]):
            print(f"  {i+1}. {dato['partido']:<15} -> {int(dato['coste']):>6} votos/escano "
                  f"(Total: {dato['escanos']} escanos)")

        mas_caro = ranking_nac[-1]
        print(f"\n  El mas caro: {mas_caro['partido']} pago {int(mas_caro['coste'])} votos "
              f"por cada uno de sus {mas_caro['escanos']} escanos.")

        print("\nA NIVEL PROVINCIAL (Top 5 escanos mas baratos de Espana):")
        for i, dato in enumerate(ranking_prov[:5]):
            print(f"  {i+1}. {dato['partido']} en {dato['provincia'].upper()} "
                  f"-> {int(dato['coste'])} votos/escano")
        print("=" * 60 + "\n")


        # --- 11. COSTE DEL ESCANO (MAS CAROS) ---
        print("\n" + "=" * 60)
        print("EL PRECIO DEL ESCANO (LOS MAS CAROS)")
        print("=" * 60)

        ranking_nac_caros, ranking_prov_caros = espana.escanos_mas_caros()

        print("\nA NIVEL NACIONAL (Top 5 partidos que pagaron mas por escano):")
        for i, dato in enumerate(ranking_nac_caros[:5]):
            print(f"  {i+1}. {dato['partido']:<15} -> {int(dato['coste']):>7} votos/escano "
                  f"(Total: {dato['escanos']} escanos)")

        print("\nA NIVEL PROVINCIAL (Top 5 escanos mas caros de Espana):")
        for i, dato in enumerate(ranking_prov_caros[:5]):
            print(f"  {i+1}. {dato['partido']} en {dato['provincia'].upper()} "
                  f"-> {int(dato['coste']):>7} votos/escano")
        print("=" * 60 + "\n")


        # --- 12. RANKING DE PROVINCIAS POR COSTE MEDIO DEL ESCANO ---
        print("\n" + "=" * 60)
        print("COSTE MEDIO DEL ESCANO POR PROVINCIA")
        print("=" * 60)

        provincias_baratas = espana.ranking_provincias_baratas()

        print("\nTOP 5 PROVINCIAS DONDE ES MAS FACIL CONSEGUIR ESCANO:")
        for i, dato in enumerate(provincias_baratas[:5]):
            print(f"  {i+1}. {dato['provincia'].upper()} ({dato['comunidad']})")
            print(f"     Media de {int(dato['coste_medio'])} votos por escano "
                  f"({dato['votos_totales']} votos para {dato['escanos_totales']} escanos)")

        print("\nTOP 5 PROVINCIAS DONDE ES MAS DIFICIL CONSEGUIR ESCANO:")
        for i, dato in enumerate(reversed(provincias_baratas[-5:])):
            print(f"  {i+1}. {dato['provincia'].upper()} ({dato['comunidad']})")
            print(f"     Media de {int(dato['coste_medio'])} votos por escano "
                  f"({dato['votos_totales']} votos para {dato['escanos_totales']} escanos)")
        print("=" * 60 + "\n")


        # --- 13. PARTIDO MAS VOTADO SIN ESCANO ---
        print("\n" + "=" * 60)
        print("PARTIDO MAS VOTADO SIN REPRESENTACION PARLAMENTARIA")
        print("=" * 60)

        sin_escano = espana.partido_mas_votado_sin_escano()

        if sin_escano:
            campeon_sin_premio = sin_escano[0]
            print(f"\nEl partido con mas votos sin escano fue: {campeon_sin_premio['partido']}")
            print(f"Obtuvo {campeon_sin_premio['votos']} votos a nivel nacional y 0 escanos.\n")

            print("Top 5 partidos extraparlamentarios con mas apoyo:")
            for i, dato in enumerate(sin_escano[:5]):
                print(f"  {i+1}. {dato['partido']:<20} -> {dato['votos']} votos")
        else:
            print("\nTodos los partidos que recibieron votos consiguieron al menos un escano.")

        print("=" * 60 + "\n")


        # --- 14. PAREJAS CON MENOS VOTOS ---
        print("\n" + "=" * 60)
        print("RESULTADOS MAS BAJOS (MAYORES QUE CERO)")
        print("=" * 60)

        n_parejas = 10
        resultados_minimos = espana.parejas_con_menos_votos(n=n_parejas)

        print(f"\nTOP {n_parejas} PARTIDOS CON MENOS VOTOS EN UNA PROVINCIA:")
        for i, dato in enumerate(resultados_minimos):
            print(f"  {i+1}. {dato['partido']} en {dato['provincia'].upper()} "
                  f"({dato['comunidad']}) -> {dato['votos']} votos")
        print("=" * 60 + "\n")


        # --- 15. PACTOMETRO ---
        print("\n" + "=" * 60)
        print("PACTOMETRO: MAYORIAS REALISTAS CON VETOS CRUZADOS")
        print("=" * 60)

        lineas_rojas = [
            ['PARTIDO POPULAR', 'PARTIDO SOCIALISTA OBRERO ESPAÑOL'],
            ['PARTIDO POPULAR', 'SUMAR'],
            ['VOX', 'PARTIDO SOCIALISTA OBRERO ESPAÑOL'],
            ['VOX', 'SUMAR'],
            ['VOX', 'EUSKAL HERRIA BILDU'],
            ['VOX', 'ESQUERRA REPUBLICANA DE CATALUNYA'],
            ['VOX', 'JUNTS PER CATALUNYA - JUNTS'],
            ['VOX', 'EUZKO ALDERDI JELTZALEA-PARTIDO NACIONALISTA VASCO'],
            ['VOX', 'BLOQUE NACIONALISTA GALEGO'],
        ]

        mayoria_absoluta = 176
        posibles_gobiernos = espana.pactometro(n=mayoria_absoluta, vetos=lineas_rojas)

        print(f"\nAplicando vetos cruzados, quedan {len(posibles_gobiernos)} vias matematicas para gobernar.")
        print("\nOPCIONES MAS SENCILLAS:")

        if posibles_gobiernos:
            for i, pacto in enumerate(posibles_gobiernos[:15]):
                alianza = " + ".join(pacto['partidos'])
                print(f"  {i+1}. {alianza}")
                print(f"     Total: {pacto['escanos_totales']} escanos")
        else:
            print("  Bloqueo electoral. Con estos vetos, ninguna combinacion alcanza la mayoria.")
            print("  Habria que repetir las elecciones.")

        print("=" * 60 + "\n")

    except FileNotFoundError:
        print(f"\n[ERROR] No se ha encontrado el archivo '{ruta_archivo}'.")
        print("Asegurate de que el archivo Excel esta en la misma carpeta que main.py.")
    except Exception as e:
        print(f"\n[ERROR] Ocurrio un fallo inesperado: {e}")


if __name__ == "__main__":
    main()
