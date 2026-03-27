import openpyxl

def generar_excel_poblacion():
    # Datos oficiales recientes del INE (aprox. 2023-2024)
    datos_poblacion = [
        ["CCAA", "Habitantes"],
        ["ANDALUCIA", 8584147],
        ["ARAGON", 1333390],
        ["PDO.ASTURIAS", 1004686],
        ["BALEARES", 1209861], # A veces viene como ILLES BALEARS, atento a tus datos
        ["CANARIAS", 2223951],
        ["CANTABRIA", 588387],
        ["CASTILLA Y LEON", 2383139],
        ["CASTILLA-LA MANCHA", 2083654],
        ["CATALUÑA", 7901963],
        ["C.VALENCIANA", 5216115], # A veces COMUNITAT VALENCIANA
        ["EXTREMADURA", 1052523],
        ["GALICIA", 2690464],
        ["MADRID", 6871903],
        ["MURCIA", 1551692],
        ["NAVARRA", 676231],
        ["PAIS VASCO", 2221080],
        ["LA RIOJA", 322282],
        ["CEUTA", 83039],
        ["MELILLA", 85491]
    ]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Poblacion 2024"

    # Escribimos los datos fila a fila
    for fila in datos_poblacion:
        ws.append(fila)

    # Guardamos el archivo
    nombre_archivo = "Poblacion_CCAA.xlsx"
    wb.save(nombre_archivo)
    print(f"¡Éxito! Archivo '{nombre_archivo}' creado en tu carpeta.")

if __name__ == "__main__":
    generar_excel_poblacion()