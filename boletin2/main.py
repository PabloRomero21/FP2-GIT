# main.py
import os
from factoria import FactoriaUniversidad

def main():
    # 1. Calculamos la ruta segura del PDF
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_pdf = os.path.join(directorio_actual, "departamentos.pdf")
    
    # 2. Fabricamos la universidad
    print("Iniciando la lectura del PDF...")
    uni = FactoriaUniversidad.leer_pdf(archivo_pdf, "Universidad de Sevilla")
    
    # 3. Probamos los métodos del enunciado
    N = 3 
    
    print(f"\n--- 1. TOP {N} DEPARTAMENTOS CON MAYOR CARGA DOCENTE ---")
    for d in uni.top_n_mayor_carga(N):
        print(f"{d.nombre} -> {d.carga_docente_real:.2f}")

    print(f"\n--- 2. TOP {N} DEPARTAMENTOS CON MENOR CARGA DOCENTE ---")
    for d in uni.top_n_menor_carga(N):
        print(f"{d.nombre} -> {d.carga_docente_real:.2f}")

    print("\n--- 3. DEPARTAMENTOS POR COEFICIENTE DE EXPERIMENTALIDAD ---")
    conteo = uni.contar_por_experimentalidad()
    for coef, cant in sorted(conteo.items()):
        print(f"Coeficiente {coef}: {cant} departamentos")

    print("\n--- 4. MEDIA DE CARGA DOCENTE POR COEFICIENTE ---")
    medias = uni.media_carga_por_experimentalidad()
    for coef, media in sorted(medias.items()):
        print(f"Coeficiente {coef}: {media:.2f} de media")

    print("\n--- 5. EXTREMOS DE MEDIAS POR EXPERIMENTALIDAD ---")
    mayor, menor = uni.extremos_media_experimentalidad()
    if mayor and menor:
        print(f"MAYOR media: Coeficiente {mayor} (Media: {medias[mayor]:.2f})")
        print(f"MENOR media: Coeficiente {menor} (Media: {medias[menor]:.2f})")

# Punto de ejecución
if __name__ == "__main__":
    main()