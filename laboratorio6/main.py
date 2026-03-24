from factoria import Factoria

def main():
    # 0. CONFIGURACIÓN Y CARGA DE DATOS
    # Asegúrate de que los nombres de los archivos coinciden exactamente con los que tienes en tu carpeta
    ruta_anexo1 = "Anexo I.xlsx"
    ruta_anexo2 = "Anexo II.xlsx"
    ruta_anexo3 = "Anexo III.xlsx"
    ruta_anexo4 = "Anexo IV.xlsx"

    print("Cargando datos de los ficheros... (Esto puede tardar unos segundos)")
    factoria = Factoria(ruta_anexo1, ruta_anexo2, ruta_anexo3, ruta_anexo4)
    
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
    # 2. ESTADÍSTICAS: TASA DE PROYECTOS CONCEDIDOS SOBRE SOLICITADOS (Por CCAA)
    # -------------------------------------------------------------------------
    print("\n2) ESTADÍSTICAS: Tasa de proyectos concedidos")
    ccaa_objetivo = "ANDALUCIA"  # Puedes cambiar esto para probar otras CCAA
    
    total_solicitados_ccaa = 0
    total_concedidos_ccaa = 0

    # Iteramos sobre TODOS los proyectos (concedidos y denegados) usando .values()
    for proyecto in gestor_general.proyectos.values():
        if proyecto.comunidad_autonoma == ccaa_objetivo:
            total_solicitados_ccaa += 1
            if proyecto.concedido: # Esta propiedad la heredan todos y vale True o False
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
    print("\n3) PRESUPUESTO CONCEDIDO (Global y por CCAA):")
    
    importe_global = 0.0
    importes_por_ccaa = {} # Diccionario para acumular dinero por comunidad

    # Solo necesitamos iterar sobre los proyectos que SÍ fueron concedidos
    for proyecto in gestor_concedidos.proyectos_concedidos.values():
        # Usamos la propiedad derivada 'presupuesto' que calcula costes directos + indirectos
        presupuesto_proyecto = proyecto.presupuesto
        
        # 1. Sumamos al global
        importe_global += presupuesto_proyecto
        
        # 2. Sumamos al acumulador de su Comunidad Autónoma específica
        ccaa = proyecto.comunidad_autonoma
        if ccaa in importes_por_ccaa:
            importes_por_ccaa[ccaa] += presupuesto_proyecto
        else:
            importes_por_ccaa[ccaa] = presupuesto_proyecto

    # Mostramos los resultados (usando formato para que los números grandes se lean bien)
    # {:,.2f} añade separadores de miles y 2 decimales.
    print(f"   - PRESUPUESTO GLOBAL CONCEDIDO: {importe_global:,.2f} €\n")
    print("   - Desglose por Comunidad Autónoma:")
    
    # Ordenamos de mayor a menor importe para que el listado quede más profesional
    for ccaa, importe in sorted(importes_por_ccaa.items(), key=lambda x: x[1], reverse=True):
        print(f"     * {ccaa}: {importe:,.2f} €")

    print("\n" + "=" * 60)

# Punto de entrada estándar en Python
if __name__ == "__main__":
    main()