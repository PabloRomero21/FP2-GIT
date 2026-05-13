
import openpyxl
from linea import Linea, Lineas

class FactoriaMetro:
    
    @staticmethod
    def leer_excel(ruta_archivo):
        lineas_metro = Lineas()
        
        try:
            workbook = openpyxl.load_workbook(ruta_archivo)
            sheet = workbook.active 
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {ruta_archivo}")
            return lineas_metro

        # Saltamos la cabecera (min_row=2)
        for fila in sheet.iter_rows(min_row=2, values_only=True):
            if not fila or fila[0] is None:
                continue
                
            nombre_linea = str(fila[0])
            estaciones_str = str(fila[1])
            total_paradas_excel = int(fila[2])
            
            # Limpieza de datos
            lista_estaciones = [estacion.strip() for estacion in estaciones_str.split(',')]
            
            # Validación
            if len(lista_estaciones) != total_paradas_excel:
                print(f"⚠️ AVISO: En {nombre_linea} se contaron {len(lista_estaciones)} paradas, pero el Excel dice {total_paradas_excel}.")
            
            # Fabricación de objetos
            nueva_linea = Linea(nombre_linea)
            for est in lista_estaciones:
                nueva_linea.agregar_parada(est)
                
            lineas_metro.agregar_linea(nueva_linea)
                
        return lineas_metro