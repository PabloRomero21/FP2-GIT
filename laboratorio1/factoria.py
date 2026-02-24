import csv
from registro import Registro

class RegistroFactory:
    @staticmethod
    def crear_desde_csv(ruta_archivo):
        """
        Lee un CSV y transforma cada fila en un objeto de la clase Registro.
        Devuelve una lista de objetos Registro.
        """
        lista_objetos = []
        try:
            with open(ruta_archivo, mode='r') as archivo:
                lector_csv = csv.reader(archivo)
                for fila in lector_csv:
                    # 'fila' es una lista de strings ['1.2', '3.4', ...]
                    # El constructor de Registro ya los convierte a float
                    nuevo_registro = Registro(fila)
                    lista_objetos.append(nuevo_registro)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo en {ruta_archivo}")
        
        return lista_objetos