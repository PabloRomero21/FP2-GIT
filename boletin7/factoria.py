import openpyxl
from nomenclator import Nomenclator

class FactoriaNomenclator:
    """
    Clase Factoría encargada de leer el archivo .xlsx y construir el Nomenclator.
    """

    @staticmethod
    def construir_nomenclator(ruta_excel):
        """
        Abre el Excel, lee las dos primeras hojas y devuelve el Nomenclator lleno.
        """
        nomenclator = Nomenclator()
        

        libro = openpyxl.load_workbook(ruta_excel, data_only=True)
        hojas = libro.sheetnames
        

        if len(hojas) >= 2:
            FactoriaNomenclator._leer_hoja(libro[hojas[0]], True, nomenclator)   # Hombres
            FactoriaNomenclator._leer_hoja(libro[hojas[1]], False, nomenclator)  # Mujeres
            
        return nomenclator

    @staticmethod
    def _leer_hoja(hoja, es_hombre, nomenclator):
        """
        Procesa una hoja concreta del Excel buscando las décadas y sus datos.
        """
        indices_decadas = []

        for col in range(1, hoja.max_column + 1):
            valor_celda = hoja.cell(row=1, column=col).value
            if valor_celda is not None:
                texto_valor = str(valor_celda).strip().upper()
                

                if "NACID" in texto_valor:

                    decada_limpia = texto_valor.replace("NACIDOS EN AÑOS ", "").replace("NACIDAS EN AÑOS ", "")
                    decada_limpia = decada_limpia.replace("NACIDOS ", "").replace("NACIDAS ", "")
                    
    
                    indices_decadas.append((col, decada_limpia))

        for fila in range(3, hoja.max_row + 1):
            
            for col_base, decada in indices_decadas:

                
                celda_nombre = hoja.cell(row=fila, column=col_base).value
                celda_frec = hoja.cell(row=fila, column=col_base + 1).value
                celda_tpm = hoja.cell(row=fila, column=col_base + 2).value
                
                if celda_nombre and str(celda_nombre).strip() != "" and str(celda_nombre).upper() != "NOMBRE":
                    try:
                        nombre_limpio = str(celda_nombre).strip()
                        
                        str_frec = str(celda_frec).replace('.', '').replace(',', '')
                        str_tpm = str(celda_tpm).replace(',', '.')
     
                        frecuencia_abs = int(float(str_frec)) 
                        tanto_por_mil = float(str_tpm)
     
                        objeto_nombre = nomenclator.obtener_nombre(nombre_limpio, es_hombre)

                        objeto_nombre.añadir_datos_decada(decada, frecuencia_abs, tanto_por_mil)
                        
                    except (ValueError, TypeError):

                        pass