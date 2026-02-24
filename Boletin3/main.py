import os
from factoriauniversidad import FactoriaUniversidad 
from factoriafacultad import FactoriaFacultad

def main():
    # 1. Calculamos la ruta segura del PDF
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_pdf = os.path.join(directorio_actual, "departamentos.pdf")
    
    # 2. Fabricamos la universidad (Lectura del PDF)
    print("Iniciando la lectura del PDF...")
    uni = FactoriaUniversidad.leer_pdf(archivo_pdf, "Universidad de Sevilla")
    print(f"✅ Se han cargado {len(uni._departamentos)} departamentos del PDF.\n")
    
    # 3. Fabricamos las Facultades (Web Scraping)
    print("Iniciando el cruce de datos con la Web (Scraping)...")
    # Este proceso crea los objetos Facultad y les asigna sus Departamentos
    diccionario_facultades = FactoriaFacultad.construir_facultades(uni._departamentos)
    
    # 4. Imprimimos el resultado final con el formato del Boletín 3
    print("\n=================================================================")
    print("🎓 EXTREMOS DE CARGA DOCENTE POR SEDE (RESULTADO BOLETÍN 3) 🎓")
    print("=================================================================\n")

    # Creamos el diccionario de extremos que pide el enunciado
    # Clave: nombre de la sede, Valor: tupla (Depto_Max, Depto_Min)
    diccionario_extremos = {}

    for facultad in diccionario_facultades.keys():
        # Llamamos al método que creaste en la clase Facultad
        # IMPORTANTE: Usar paréntesis () para ejecutar el método
        extremos = facultad.obtener_extremos_carga() 
        diccionario_extremos[facultad.nombre] = extremos

    # 5. Mostramos la información de forma legible
    for sede, tupla_deptos in diccionario_extremos.items():
        depto_mayor, depto_menor = tupla_deptos
        
        print(f"Sede: {sede}")
        
        if depto_mayor and depto_menor:
            # Formateamos los números a 2 decimales para que queden profesionales
            c_max = f"{depto_mayor.carga_docente_real:.2f}"
            c_min = f"{depto_menor.carga_docente_real:.2f}"
            
            print(f"  Departamento con MAYOR carga: {depto_mayor.nombre} (Carga: {c_max})")
            print(f"  Departamento con MENOR carga: {depto_menor.nombre} (Carga: {c_min})")
        else:
            print("  Sin datos suficientes en esta sede.")
            
        print("-" * 75)

    print("\n✅ Proceso finalizado con éxito.")

# Punto de ejecución
if __name__ == "__main__":
    main()