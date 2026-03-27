from factoria import Factoria

def main():
    # 0. CONFIGURACIÓN Y CARGA DE DATOS
    ruta_anexo1 = "Anexo I.xlsx"
    ruta_anexo2 = "Anexo II.xlsx"
    ruta_anexo3 = "Anexo III.xlsx"
    ruta_anexo4 = "Anexo IV.xlsx"
    ruta_poblacion = "Poblacion_CCAA.xlsx" # Añadimos el nuevo archivo de población

    print("Cargando datos de los ficheros... (Esto puede tardar unos segundos)")
    # Le pasamos los 5 archivos a la factoría
    factoria = Factoria(ruta_anexo1, ruta_anexo2, ruta_anexo3, ruta_anexo4, ruta_poblacion)
    
    # Recibimos los tres gestores ya poblados
    gestor_general, gestor_concedidos, gestor_contratos = factoria.procesar_datos()
    
    print("¡Datos cargados correctamente!\n")
    print("=" * 60)

    # -------------------------------------------------------------------------
    # 1. MOSTRAR EL TOTAL DE REGISTROS ALMACENADOS EN CADA CLASE GESTOR
    # -------------------------------------------------------------------------
    print("\n1) TOTAL DE REGISTROS ALMACENADOS:")
    print(f"   - Proyectos Totales (Gestor_Proyectos): {gestor_general.obtener_total()}")
    print(f"   - Proyectos Concedidos (Gestor_ProyectosConcedidos): {gestor_concedidos.obtener_total()}")
    print(f"   - Proyectos con Contrato (Gestor_ProyectosContrato): {gestor_contratos.obtener_total()}")


    # -------------------------------------------------------------------------
    # 2. ESTADÍSTICAS: TASA DE PROYECTOS CONCEDIDOS SOBRE SOLICITADOS (Ejemplo CCAA)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("2) ESTADÍSTICAS BÁSICAS (Ejemplo Andalucía)")
    print("=" * 60)
    
    # Usamos la lógica antigua temporalmente para este ejemplo rápido, 
    # aunque en el punto 4 lo hacemos para todas de forma más profesional.
    ccaa_objetivo = "ANDALUCIA"
    total_solicitados_ccaa = 0
    total_concedidos_ccaa = 0

    for proyecto in gestor_general.proyectos.values():
        if proyecto.comunidad_autonoma == ccaa_objetivo:
            total_solicitados_ccaa += 1
            if proyecto.concedido:
                total_concedidos_ccaa += 1

    if total_solicitados_ccaa > 0:
        tasa_exito = (total_concedidos_ccaa / total_solicitados_ccaa) * 100
        print(f"   Comunidad Autónoma: {ccaa_objetivo}")
        print(f"   - Proyectos Solicitados: {total_solicitados_ccaa}")
        print(f"   - Proyectos Concedidos: {total_concedidos_ccaa}")
        print(f"   - Tasa de Éxito: {tasa_exito:.2f}%")
    else:
        print(f"   No hay datos para la CCAA: {ccaa_objetivo}")


    # -------------------------------------------------------------------------
    # 3. TOTAL DE IMPORTES GLOBAL Y POR COMUNIDAD AUTÓNOMA
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("3) PRESUPUESTO CONCEDIDO (Global y por CCAA)")
    print("=" * 60)
    
    importe_global = 0.0
    importes_por_ccaa = {} 

    for proyecto in gestor_concedidos.proyectos_concedidos.values():
        presupuesto_proyecto = proyecto.presupuesto
        importe_global += presupuesto_proyecto
        
        ccaa = proyecto.comunidad_autonoma
        if ccaa in importes_por_ccaa:
            importes_por_ccaa[ccaa] += presupuesto_proyecto
        else:
            importes_por_ccaa[ccaa] = presupuesto_proyecto

    print(f"   - PRESUPUESTO GLOBAL CONCEDIDO: {importe_global:,.2f} €\n")
    print("   - Desglose por Comunidad Autónoma:")
    
    for ccaa, importe in sorted(importes_por_ccaa.items(), key=lambda x: x[1], reverse=True):
        print(f"     * {ccaa}: {importe:,.2f} €")


    # -------------------------------------------------------------------------
    # 4. TASAS DE ÉXITO POR COMUNIDAD AUTÓNOMA (Concedidos y Contratos)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("4) TASAS DE ÉXITO GLOBALES POR COMUNIDAD AUTÓNOMA")
    print("=" * 60)
    
    # Le pedimos al gestor que haga los cálculos matemáticos pesados
    datos_estadisticos = gestor_general.calcular_tasas_exito_ccaa()
    
    # El main solo se preocupa de ponerlo bonito en pantalla (ordenado alfabéticamente)
    for ccaa in sorted(datos_estadisticos.keys()):
        datos = datos_estadisticos[ccaa]
        print(f"📍 {ccaa}")
        print(f"   - Solicitados: {datos['solicitados']}")
        print(f"   - Concedidos:  {datos['concedidos']} ({datos['tasa_concedidos']:.2f}%)")
        print(f"   - c/ Contrato: {datos['contratos']} ({datos['tasa_contratos']:.2f}%)\n")


    # -------------------------------------------------------------------------
    # 5. TASA DE FINANCIACIÓN POR HABITANTE (€/hab)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("5) TASA DE FINANCIACIÓN POR HABITANTE (€/hab)")
    print("=" * 60)
    
    # Pedimos los datos al gestor (ya no le pasamos ruta, usa sus datos internos)
    financiacion_per_capita = gestor_general.calcular_financiacion_por_habitante()
    
    # Ordenamos el diccionario por la 'tasa_per_capita' de mayor a menor
    ccaa_ordenadas = sorted(
        financiacion_per_capita.items(), 
        key=lambda x: x[1]['tasa_per_capita'], 
        reverse=True
    )
    
    for ccaa, datos in ccaa_ordenadas:
        if datos['habitantes'] > 0:
            print(f"📍 {ccaa}:")
            print(f"   - Presupuesto Total: {datos['presupuesto']:,.2f} €")
            print(f"   - Habitantes: {datos['habitantes']:,}".replace(',', '.')) # Formato español para miles
            print(f"   - INVERSIÓN PER CÁPITA: {datos['tasa_per_capita']:.2f} € por habitante\n")
        else:
            print(f"📍 {ccaa}: ⚠️ AVISO - No se encontró la población. Revisa el nombre en el Excel de población.\n")


# -------------------------------------------------------------------------
    # 6. TOP 'N' ENTIDADES CON MAYOR TASA DE ÉXITO
    # -------------------------------------------------------------------------
    # 1. Defines tu parámetro 'n' directamente en el código
    n_param = 30  # <-- Puedes cambiar este número por 5, 20, o lo que necesites
    
    print("\n" + "=" * 60)
    print(f"6) RANKING: TOP {n_param} ENTIDADES CON MAYOR TASA DE ÉXITO")
    print("=" * 60)

    # 2. Llamamos al gestor pasándole el parámetro directamente
    top_concedidos, top_contratos = gestor_general.obtener_top_n_entidades_exito(n_param)

    # 3. Imprimimos el primer ranking
    print(f"\n🏆 TOP {n_param} - MAYOR TASA DE PROYECTOS CONCEDIDOS:")
    print("-" * 60)
    for i, datos in enumerate(top_concedidos, start=1):
        print(f"{i}. {datos['entidad']}")
        print(f"   Tasa: {datos['tasa_concedidos']:.2f}% ({datos['concedidos']} concedidos de {datos['solicitados']} solicitados)")

    # 4. Imprimimos el segundo ranking
    print(f"\n🎓 TOP {n_param} - MAYOR TASA DE PROYECTOS CON CONTRATO:")
    print("-" * 60)
    for i, datos in enumerate(top_contratos, start=1):
        print(f"{i}. {datos['entidad']}")
        print(f"   Tasa: {datos['tasa_contratos']:.2f}% ({datos['contratos']} con contrato de {datos['solicitados']} solicitados)\n")


    # -------------------------------------------------------------------------
    # 7. ESTUDIO DE TASAS DE ÉXITO POR ÁREAS Y MACROÁREAS (AEI)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("7) TASAS DE ÉXITO POR MACROÁREAS DE CONOCIMIENTO (AEI)")
    print("=" * 60)
    
    tasas_macro = gestor_general.obtener_tasa_exito_por_macroarea()
    
    # Ordenamos de mayor a menor tasa de éxito de concesión
    for macro, datos in sorted(tasas_macro.items(), key=lambda x: x[1]['tasa_concedidos'], reverse=True):
        print(f"🔬 {macro}:")
        print(f"   - Solicitados: {datos['solicitados']}")
        print(f"   - Concedidos:  {datos['concedidos']} (Tasa: {datos['tasa_concedidos']:.2f}%)")
        print(f"   - c/ Contrato: {datos['contratos']} (Tasa: {datos['tasa_contratos']:.2f}%)\n")

    print("\n" + "=" * 60)
    print("8) TASAS DE ÉXITO POR ÁREAS TEMÁTICAS (AEI)")
    print("=" * 60)
    
    tasas_area = gestor_general.obtener_tasa_exito_por_area()
    
    # Mostramos el top 10 de áreas con mayor éxito (para no llenar la consola)
    top_areas = sorted(tasas_area.items(), key=lambda x: x[1]['tasa_concedidos'], reverse=True)
    
    for area, datos in top_areas:
        # Filtramos para quitar "OTROS" si quieres un ranking limpio
        if area != "OTROS / SIN CLASIFICAR":
            print(f"📚 {area}")
            print(f"   Tasa Concesión: {datos['tasa_concedidos']:.2f}% | Tasa Contratos: {datos['tasa_contratos']:.2f}% (de {datos['solicitados']} solicitados)")


# Punto de entrada estándar en Python
if __name__ == "__main__":
    main()