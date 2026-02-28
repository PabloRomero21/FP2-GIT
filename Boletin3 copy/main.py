# main.py
import os
from factoriapdf import Factoriapdf
from factoriafacultad import FactoriaFacultad
from universidad import Universidad

def main():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_pdf = os.path.join(directorio_actual, "departamentos.pdf")
    
    # 1. Extraer materia prima (Lectura del PDF)
    print("Iniciando la lectura del PDF...")
    departamentos_sueltos = Factoriapdf.extraer_departamentos_pdf(archivo_pdf)
    
    # 2. Construir Facultades cruzando con la Web (Scraping)
    print("Iniciando el cruce de datos con la Web (Scraping)...")
    lista_facultades = FactoriaFacultad.construir_facultades(departamentos_sueltos)
    
    # 3. Ensamblar la Universidad
    uni_sevilla = Universidad("Universidad de Sevilla")
    for facultad in lista_facultades:
        uni_sevilla.agregar_facultad(facultad)
        
    # 4. Imprimir resultados (Requisito Boletín 3)
    print("\n=================================================================")
    print("🎓 EXTREMOS DE CARGA DOCENTE POR SEDE (RESULTADO BOLETÍN 3) 🎓")
    print("=================================================================\n")
    
    diccionario_extremos = uni_sevilla.generar_diccionario_extremos_sedes()
    
    for sede, tupla_deptos in diccionario_extremos.items():
        depto_mayor, depto_menor = tupla_deptos
        
        print(f"Sede: {sede}")
        
        if depto_mayor and depto_menor:
            c_max = f"{depto_mayor.carga_docente_real:.2f}" if depto_mayor.carga_docente_real != float('inf') else "Inf"
            c_min = f"{depto_menor.carga_docente_real:.2f}" if depto_menor.carga_docente_real != float('inf') else "Inf"
            
            print(f"  Departamento con MAYOR carga: {depto_mayor.nombre} (Carga: {c_max})")
            print(f"  Departamento con MENOR carga: {depto_menor.nombre} (Carga: {c_min})")
        else:
            print("  Sin datos suficientes en esta sede.")
            
        print("-" * 75)

    


    print("\n" + "="*75)
    print("📊 MEDIA PONDERADA DE CARGA DOCENTE POR SEDE (BOLETÍN 3)")
    print("="*75)
    
    medias = uni_sevilla.generar_diccionario_medias_ponderadas()
    for sede, valor in medias.items():
        print(f"📍 {sede:<60} | Media: {valor:>6.2f}")


    print("\n✅ Proceso finalizado con éxito.")

if __name__ == "__main__":
    main()