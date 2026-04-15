from factoria import FactoriaNomenclator

def main():
    # 1. Definimos los nombres de los archivos
    # El archivo de entrada debe ser el original del INE
    archivo_entrada = "frecuencia_nombres.xlsx"
    # El archivo de salida será el que cree nuestro programa
    archivo_salida = "nomenclator_exportado.xlsx"

    print(f"--- Iniciando prueba de exportación ---")

    try:
        # 2. Cargamos los datos a través de la Factoría
        print(f"Leyendo datos desde '{archivo_entrada}'...")
        nomenclator = FactoriaNomenclator.construir_nomenclator(archivo_entrada)
        
        # Verificación rápida de carga
        total_registros = len(nomenclator.nombres)
        if total_registros == 0:
            print("Aviso: No se han cargado nombres. Revisa que el Excel de entrada sea correcto.")
            return

        print(f"Carga exitosa. Se han procesado {total_registros} registros únicos.")

        # 3. Probamos el nuevo método de exportación
        print(f"Generando nuevo archivo Excel: '{archivo_salida}'...")
        nomenclator.exportar_a_excel(archivo_salida)
        
        print("\n" + "="*50)
        print("¡OPERACIÓN COMPLETADA CON ÉXITO!")
        print(f"Se ha creado el archivo '{archivo_salida}' en esta misma carpeta.")
        print("Ábrelo para comprobar que cada fila tiene su género y todas sus décadas.")
        print("="*50)

# --- PRUEBA: NOMBRE MÁS FRECUENTE ABSOLUTO ---
        print("\n" + "=" * 50)
        print("NOMBRE CON MAYOR FRECUENCIA ABSOLUTA EN TODAS LAS DÉCADAS:")
        
        max_ambos = nomenclator.nombre_mas_frecuente(es_hombre=None)
        if max_ambos:
            print(f"Ambos géneros: {max_ambos.texto} con {max_ambos.frecuencia_acumulada} nacimientos.")

        max_hombre = nomenclator.nombre_mas_frecuente(es_hombre=True)
        if max_hombre:
            print(f"Hombres: {max_hombre.texto} con {max_hombre.frecuencia_acumulada} nacimientos.")

        max_mujer = nomenclator.nombre_mas_frecuente(es_hombre=False)
        if max_mujer:
            print(f"Mujeres: {max_mujer.texto} con {max_mujer.frecuencia_acumulada} nacimientos.")
        print("=" * 50)


        # --- PRUEBA: LOS N NOMBRES MÁS USADOS ---
        print("\n" + "=" * 50)
        
        print("TOP 5 NOMBRES MÁS USADOS (AMBOS GÉNEROS):")
        top_5_ambos = nomenclator.n_nombres_mas_usados(5, es_hombre=None)
        for i, obj in enumerate(top_5_ambos):
            print(f"{i+1}º - {obj.texto} con {obj.frecuencia_acumulada} nacimientos")

        print("\nTOP 3 NOMBRES MÁS USADOS (MUJERES):")
        top_3_mujeres = nomenclator.n_nombres_mas_usados(3, es_hombre=False)
        for i, obj in enumerate(top_3_mujeres):
            print(f"{i+1}º - {obj.texto} con {obj.frecuencia_acumulada} nacimientos")
            
        print("=" * 50)



        # --- PRUEBA: FRECUENCIAS DE INICIALES POR DÉCADA ---
        print("\n" + "=" * 50)
        print("EVOLUCIÓN HISTÓRICA DE LA INICIAL 'M' (MUJERES):")
        
        # Generamos el diccionario solo para mujeres
        dic_iniciales_decada = nomenclator.frecuencias_iniciales_por_decada(es_hombre=False)
        
        # Comprobamos cómo han evolucionado los nombres que empiezan por 'M'
        if 'M' in dic_iniciales_decada:
            for decada, total_frec in dic_iniciales_decada['M']:
                print(f" - {decada}: {total_frec} nacimientos")
                
        print("=" * 50)



        # --- PRUEBA: INICIAL MÁS FRECUENTE POR DÉCADA ---
        print("\n" + "=" * 50)
        print("LETRA INICIAL MÁS FRECUENTE POR DÉCADA (HOMBRES):")
        
        letras_decada_hombres = nomenclator.inicial_mas_frecuente_por_decada(es_hombre=True)
        
        for decada, datos in letras_decada_hombres.items():
            letra = datos[0]
            porcentaje = datos[1]
            print(f" - {decada}: La letra '{letra}' dominó con un {porcentaje}% de los nombres.")
            
        print("=" * 50)


        # --- PRUEBA: EVOLUCIÓN DE NOMBRES COMPUESTOS ---
        print("\n" + "=" * 50)
        print("EVOLUCIÓN DE NOMBRES SIMPLES VS COMPUESTOS (AMBOS GÉNEROS):")
        
        evolucion = nomenclator.evolucion_nombres_compuestos()
        
        # Cabecera de la tabla
        print(f"{'DÉCADA':<25} | {'% SIMPLE':<10} | {'% COMPUESTO':<10}")
        print("-" * 55)
        
        for decada, p_simple, p_compuesto in evolucion:
            print(f"{decada:<25} | {p_simple:>8}% | {p_compuesto:>10}%")
            
        print("=" * 50)


        # --- PRUEBA: LONGITUD MEDIA DE LOS NOMBRES ---
        print("\n" + "=" * 50)
        print("EVOLUCIÓN DE LA LONGITUD MEDIA DE LOS NOMBRES (MUJERES):")
        
        evolucion_longitud = nomenclator.longitud_media_por_decada(es_hombre=False)
        
        for decada, media in evolucion_longitud:
            print(f" - {decada}: {media} letras de media por bebé")
            
        print("\nEVOLUCIÓN DE LA LONGITUD MEDIA DE LOS NOMBRES (HOMBRES):")
        
        evolucion_longitud_h = nomenclator.longitud_media_por_decada(es_hombre=True)
        
        for decada, media in evolucion_longitud_h:
            print(f" - {decada}: {media} letras de media por bebé")
            
        print("=" * 50)


        # --- PRUEBA: NOMBRES EN AL MENOS 'N' DÉCADAS ---
        print("\n" + "=" * 50)
        
        # En nuestro Excel hay un total de 11 décadas históricas.
        # Vamos a buscar nombres muy "persistentes" que hayan aguantado al menos 10 décadas.
        n_buscado = 10 
        
        print(f"NOMBRES DE MUJER EN EL TOP 50 DURANTE AL MENOS {n_buscado} DÉCADAS:")
        mujeres_persistentes = nomenclator.nombres_en_n_decadas(n_buscado, es_hombre=False)
        
        if mujeres_persistentes:
            for obj in mujeres_persistentes:
                print(f" - {obj.texto}: {len(obj.datos_por_decada)} décadas (Total: {obj.frecuencia_acumulada})")
        else:
            print("Ningún nombre cumplió la condición.")

        print(f"\nNOMBRES DE HOMBRE EN EL TOP 50 DURANTE TODAS LAS DÉCADAS (11):")
        # Aquí probamos a buscar los que han estado en TODAS (11 décadas)
        hombres_historicos = nomenclator.nombres_en_n_decadas(11, es_hombre=True)
        
        if hombres_historicos:
            for obj in hombres_historicos:
                print(f" - {obj.texto}: {len(obj.datos_por_decada)} décadas (Total: {obj.frecuencia_acumulada})")
        else:
            print("Ningún nombre cumplió la condición.")
            
        print("=" * 50)


        # --- PRUEBA: MODAS PASAJERAS (NOMBRES OLVIDADOS) ---
        print("\n" + "=" * 50)
        
        # Vamos a buscar nombres que estuvieron de moda solo en las primeras 3 décadas 
        # (Antes de 1930, 1930-1939, 1940-1949) y luego desaparecieron del Top 50.
        n_decadas = 3 
        
        print(f"HOMBRES QUE PASARON AL OLVIDO TRAS LAS {n_decadas} PRIMERAS DÉCADAS:")
        olvidados_hombres = nomenclator.modas_pasajeras_al_principio(n_decadas, es_hombre=True)
        
        if olvidados_hombres:
            # Imprimimos solo los 5 primeros para no saturar la pantalla
            for obj in olvidados_hombres[:5]:
                print(f" - {obj.texto} (Sobrevivió {len(obj.datos_por_decada)} décadas tempranas)")
        else:
            print("Ningún nombre cumplió la condición.")

        print(f"\nMUJERES QUE PASARON AL OLVIDO TRAS LAS {n_decadas} PRIMERAS DÉCADAS:")
        olvidados_mujeres = nomenclator.modas_pasajeras_al_principio(n_decadas, es_hombre=False)
        
        if olvidados_mujeres:
            for obj in olvidados_mujeres[:5]:
                print(f" - {obj.texto} (Sobrevivió {len(obj.datos_por_decada)} décadas tempranas)")
        else:
            print("Ningún nombre cumplió la condición.")
            
        print("=" * 50)


        # --- PRUEBA: MODAS RECIENTES ---
        print("\n" + "=" * 50)
        
        # Vamos a buscar nombres que han irrumpido en el Top 50 
        # exclusivamente en las últimas 3 décadas (2000s, 2010s, 2020s)
        n_decadas_recientes = 3 
        
        print(f"HOMBRES QUE SON MODA EN LAS ÚLTIMAS {n_decadas_recientes} DÉCADAS:")
        recientes_hombres = nomenclator.modas_recientes(n_decadas_recientes, es_hombre=True)
        
        if recientes_hombres:
            # Imprimimos los 5 primeros
            for obj in recientes_hombres[:5]:
                print(f" - {obj.texto} (Total nacimientos: {obj.frecuencia_acumulada})")
        else:
            print("Ningún nombre cumplió la condición.")

        print(f"\nMUJERES QUE SON MODA EN LAS ÚLTIMAS {n_decadas_recientes} DÉCADAS:")
        recientes_mujeres = nomenclator.modas_recientes(n_decadas_recientes, es_hombre=False)
        
        if recientes_mujeres:
            for obj in recientes_mujeres[:5]:
                print(f" - {obj.texto} (Total nacimientos: {obj.frecuencia_acumulada})")
        else:
            print("Ningún nombre cumplió la condición.")
            
        print("=" * 50)



        # --- PRUEBA: NOMBRES RESURGIDOS (EL EFECTO VINTAGE) ---
        print("\n" + "=" * 50)
        
        # Vamos a buscar nombres que estuvieron 2 décadas seguidas de moda, 
        # desaparecieron 3 décadas seguidas, y luego volvieron al Top 50.
        n_presencia = 2
        m_ausencia = 3
        
        print(f"HOMBRES QUE RESURGIERON (Patrón: {n_presencia} de moda, {m_ausencia} olvidados, y vuelta):")
        resurgidos_hombres = nomenclator.nombres_resurgidos(n_presencia, m_ausencia, es_hombre=True)
        
        if resurgidos_hombres:
            for obj in resurgidos_hombres:
                print(f" - {obj.texto} (Total nacimientos: {obj.frecuencia_acumulada})")
        else:
            print("Ningún nombre de hombre cumplió esta condición exacta.")

        print(f"\nMUJERES QUE RESURGIERON (Patrón: {n_presencia} de moda, {m_ausencia} olvidadas, y vuelta):")
        resurgidos_mujeres = nomenclator.nombres_resurgidos(n_presencia, m_ausencia, es_hombre=False)
        
        if resurgidos_mujeres:
            for obj in resurgidos_mujeres:
                print(f" - {obj.texto} (Total nacimientos: {obj.frecuencia_acumulada})")
        else:
            print("Ningún nombre de mujer cumplió esta condición exacta.")
            
        print("=" * 50)


# --- PRUEBA: GUARDAR GRÁFICA EN DISCO ---
        print("\n" + "=" * 50)
        print("GENERANDO ARCHIVO PNG CON LA GRÁFICA...")
        
        nombres_interesantes = ["ANTONIO", "MARIA", "LUCIA", "MATEO"]
        
        # Guardamos la comparativa en un archivo llamado 'comparativa_nombres.png'
        nomenclator.guardar_grafica_tendencia_tpm(
            nombres_interesantes, 
            nombre_archivo="comparativa_nombres.png"
        )
        
        print("Ya puedes buscar el archivo 'comparativa_nombres.png' en la carpeta de tu proyecto.")
        print("=" * 50)


        # --- PRUEBA: MAYOR INCREMENTO ENTRE DÉCADAS ---
        print("\n" + "=" * 50)
        
        n_tops = 5
        print(f"LOS {n_tops} NOMBRES QUE PEGARON EL MAYOR SALTO DE POPULARIDAD:")
        
        mayores_saltos = nomenclator.mayor_incremento_tpm(n_tops, es_hombre=None)
        
        for i, datos in enumerate(mayores_saltos):
            obj = datos['objeto']
            inc = round(datos['incremento'], 2)
            desde = datos['desde']
            hasta = datos['hasta']
            genero = "Hombre" if obj.es_hombre else "Mujer"
            
            print(f"{i+1}º - {obj.texto} ({genero})")
            print(f"     Subió +{inc}‰ puntos pasando de '{desde}' a '{hasta}'")
            
        print("=" * 50)


        # --- PRUEBA: DIVERSIFICACIÓN (CONCENTRACIÓN DEL TOP N) ---
        print("\n" + "=" * 50)
        
        n_top = 10
        print(f"CONCENTRACIÓN: SUMA DEL TPM DE LOS {n_top} NOMBRES MÁS COMUNES")
        print("(Si el número baja, significa que hay más variedad de nombres)")
        
        print("\nMUJERES:")
        concentracion_mujeres = nomenclator.concentracion_top_n(n_top, es_hombre=False)
        for decada, suma_tpm in concentracion_mujeres.items():
            print(f" - {decada}: {suma_tpm}‰ de las niñas nacidas")

        print("\nHOMBRES:")
        concentracion_hombres = nomenclator.concentracion_top_n(n_top, es_hombre=True)
        for decada, suma_tpm in concentracion_hombres.items():
            print(f" - {decada}: {suma_tpm}‰ de los niños nacidos")
            
        print("=" * 50)


        # --- PRUEBA: GRÁFICA DE DIVERSIFICACIÓN EN PNG ---
        print("\n" + "=" * 50)
        print("GENERANDO ARCHIVO PNG DE LA GRÁFICA DE CONCENTRACIÓN...")
        
        n_top_grafica = 10
        archivo_salida = "grafica_diversificacion.png"
        
        # Al no pasarle "es_hombre", nos dibujará ambas líneas para comparar
        nomenclator.guardar_grafica_concentracion(
            n_top_grafica, 
            nombre_archivo=archivo_salida
        )
        
        print(f"Ya puedes buscar el archivo '{archivo_salida}' en tu carpeta.")
        print("Nota: Verás que la línea baja con el tiempo. Eso significa que")
        print("el total del 'pastel' que se llevan los nombres top es menor,")
        print("es decir, la sociedad cada vez elige nombres más variados.")
        print("=" * 50)

    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo '{archivo_entrada}'. Asegúrate de que esté en la misma carpeta que este script.")
    except Exception as e:
        print(f"Ha ocurrido un error durante el proceso: {e}")


    

if __name__ == "__main__":
    main()