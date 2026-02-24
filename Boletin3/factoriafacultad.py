import requests
from bs4 import BeautifulSoup
import unicodedata

from facultad import Facultad
from departamento import Departamento

class FactoriaFacultad:
    """Clase Factoría encargada de construir las Facultades cruzando datos mediante Web Scraping."""

    @staticmethod
    def _normalizar_nombre(nombre: str) -> str:
        """
        Transforma el nombre del departamento del PDF al formato URL.
        Ej: "DEPARTAMENTO DE ÁLGEBRA" -> "algebra"
        """
        # 1. Convertir a minúsculas y eliminar espacios a los lados
        nombre_limpio = nombre.lower().strip().replace(",", "").replace("(", "").replace(")", "")
        
        # 2. Eliminar la subcadena "departamento de " si existe al principio
        prefijo = "departamento de "
        if nombre_limpio.startswith(prefijo):
            # Recortamos el texto desde donde acaba el prefijo en adelante
            nombre_limpio = nombre_limpio[len(prefijo):].strip()
            
        # 3. Eliminar las tildes (acentos). 
        # Esto es vital porque en las URL no se usan tildes (educación -> educacion)
        nombre_limpio = ''.join(
            c for c in unicodedata.normalize('NFD', nombre_limpio)
            if unicodedata.category(c) != 'Mn'
        )
        
        # 4. Sustituir los espacios en blanco por guiones (-)
        # Usamos split() y join() para asegurarnos de que si hay 2 espacios seguidos, los trate bien
        nombre_normalizado = "-".join(nombre_limpio.split())
        
        if nombre_normalizado == "ciencias-juridicas-basicas":

            nombre_normalizado = "ciencias-juridicas-basicas-derecho-romano-historia-del-derecho-y-derecho"

        return nombre_normalizado

    @classmethod
    def construir_facultades(cls, lista_departamentos: list) -> dict:
        """
        Recibe una lista de objetos Departamento, busca su sede web y los agrupa.
        Retorna un diccionario: {Objeto_Facultad: [Lista_Objetos_Departamento]}
        """
        # Usaremos este diccionario intermedio para buscar de forma rápida 
        # (por nombre de texto) si ya hemos creado la Facultad previamente.
        registro_facultades_por_nombre = {}
        
        url_base = "https://www.us.es/centros/departamentos/"
        
        print(f"Iniciando scraping para {len(lista_departamentos)} departamentos. Esto tomará un tiempo...")
        
        # 2. Recorremos la lista departamento a departamento
        for depto in lista_departamentos:
            
            # 3. Normalizamos el nombre
            nombre_url = cls._normalizar_nombre(depto.nombre)
            
            # 4. Construimos la URL completa
            url_completa = url_base + nombre_url
            print(f" -> Consultando: {url_completa}")
            
            # 5. y 6. Realizamos la petición web
            try:
                respuesta = requests.get(url_completa)
                nombre_sede = "Sede Desconocida" # Por si la web no tiene la etiqueta
                
                if respuesta.status_code == 200:
                    sopa = BeautifulSoup(respuesta.text, 'html.parser')
                    etiqueta_sede = sopa.find('h3', string='Sede')
                    
                    if etiqueta_sede:
                        enlace_facultad = etiqueta_sede.find_next('a')
                        if enlace_facultad:
                            nombre_sede = enlace_facultad.text.strip()
                else:
                    print(f"    [!] Error {respuesta.status_code}. No se encontró la URL.")
                    
            except requests.RequestException as e:
                print(f"    [!] Error de red: {e}")
                nombre_sede = "Sede Desconocida"

            # 7. Creación o recuperación del objeto Facultad
            # Comprobamos si ya habíamos instanciado una Facultad con este nombre
            if nombre_sede not in registro_facultades_por_nombre:
                # Si no existe, creamos el objeto Facultad
                nueva_facultad = Facultad(nombre_sede)
                # Lo guardamos en nuestro registro de control
                registro_facultades_por_nombre[nombre_sede] = nueva_facultad
            
            # Recuperamos el objeto Facultad (ya sea el nuevo que acabamos de crear, o el que ya existía)
            facultad_objetivo = registro_facultades_por_nombre[nombre_sede]
            
            # Añadimos el departamento a la lista interna del objeto Facultad (usando el método seguro)
            facultad_objetivo.agregar_departamento(depto)

        # 8. Construimos el formato exacto de salida que me has pedido
        # "las claves seran los objetos facultad y los valores seran la lista de departamentos"
        diccionario_resultado = {}
        
        for objeto_facultad in registro_facultades_por_nombre.values():
            # Accedemos al atributo protegido para montar el diccionario final
            diccionario_resultado[objeto_facultad] = objeto_facultad._departamentos
            
        return diccionario_resultado