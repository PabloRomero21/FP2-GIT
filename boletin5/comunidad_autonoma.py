class ComunidadAutonoma:
    def __init__(self, nombre, lista_provincias=None):
        self.nombre = nombre
        
        # Inicializamos el diccionario vacío internamente
        self.provincias = {}
        
        # Si recibimos la lista de tuplas (id, objeto_provincia), la procesamos
        if lista_provincias is not None:
            for id_provincia, objeto_provincia in lista_provincias:
                self.provincias[id_provincia] = objeto_provincia