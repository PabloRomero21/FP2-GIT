# universidad.py

class Universidad:
    """Clase base que gestiona la colección de facultades."""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._facultades = []     

    def agregar_facultad(self, facultad: 'Facultad'):
        """Añade un objeto Facultad a la lista de la universidad."""
        self._facultades.append(facultad)

    def generar_diccionario_extremos_sedes(self) -> dict:
        """Crea y devuelve el diccionario de extremos de carga por sede."""
        diccionario_extremos = {}
        for facultad in self._facultades:
            extremos = facultad.obtener_extremos_carga() 
            diccionario_extremos[facultad.nombre] = extremos
        return diccionario_extremos

    


