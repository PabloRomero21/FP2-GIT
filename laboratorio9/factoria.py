import pandas as pd
from dataset import DataSetRegresion
from registro import RegistroRegresion

class FactoriaSerieTemporal:
    @staticmethod
    def leer_fichero(ruta):
        """Lee el XLSX usando pandas."""
        try:
            # Leemos el excel, asumiendo que los datos están en la columna 'Valor'
            df = pd.read_excel(ruta)
            return df['Valor'].astype(float).tolist()
        except Exception as e:
            print(f"Error al leer el archivo Excel {ruta}: {e}")
            return []

    @staticmethod
    def leer_fichero_y_crear_dataset(ruta, ph):
        valores = FactoriaSerieTemporal.leer_fichero(ruta)
        if not valores:
            return None

        ds = DataSetRegresion()
        cabeceras = [f"Lag_{i}" for i in range(ph, 0, -1)] + ["Objetivo"]
        ds.set_cabeceras(cabeceras)

        for i in range(len(valores) - ph):
            ventana = valores[i : i + ph]
            objetivo = valores[i + ph]
            ds.agregar_registro(RegistroRegresion(ventana, objetivo))
        
        return ds