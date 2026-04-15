class DatosDecada:
    """
    Clase para agrupar la frecuencia y el tanto por mil de una década específica.
    """
    def __init__(self, decada, frecuencia_abs, tanto_por_mil):
        self.decada = decada
        self.frecuencia_abs = frecuencia_abs
        self.tanto_por_mil = tanto_por_mil

class Nombre:
    def __init__(self, texto, es_hombre):
        # El nombre de pila (ej: "Juan")[cite: 4].
        self.texto = texto
        # Propiedad que indica si es de hombre o mujer[cite: 8].
        self.es_hombre = es_hombre
        # Lista que asocia el nombre con sus datos por década.
        # Si no está entre los 50 más frecuentes, no se añade a esta lista[cite: 7].
        self.datos_por_decada = []

    def añadir_datos_decada(self, decada, frecuencia_abs, tanto_por_mil):
        """
        Crea un objeto con los datos de la década y lo añade a la lista.
        """
        nuevo_dato = DatosDecada(decada, frecuencia_abs, tanto_por_mil)
        self.datos_por_decada.append(nuevo_dato)

    @property
    def frecuencia_acumulada(self):
        """
        Propiedad derivada que suma la frecuencia absoluta de todas las décadas.
        """
        total = 0
        for dato in self.datos_por_decada:
            total += dato.frecuencia_abs
        return total

    def __repr__(self):
        genero = "Hombre" if self.es_hombre else "Mujer"
        return f"Nombre: {self.texto} ({genero}) - Total: {self.frecuencia_acumulada}"