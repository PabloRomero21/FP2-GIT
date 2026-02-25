# factoriafacultad.py
import requests
from bs4 import BeautifulSoup
import unicodedata
import time

from facultad import Facultad
from departamento import Departamento

class Factoria:
    """Factoría encargada de construir las Facultades cruzando datos mediante Web Scraping."""

    @staticmethod
    def _normalizar_nombre(nombre: str) -> str:
        nombre_limpio = nombre.lower().strip().replace(",","").replace("(","").replace(")","")
        prefijo = "departamento de "
        if nombre_limpio.startswith(prefijo):
            nombre_limpio = nombre_limpio[len(prefijo):].strip()
            
        nombre_limpio = ''.join(
            c for c in unicodedata.normalize('NFD', nombre_limpio)
            if unicodedata.category(c) != 'Mn'
        )

        cola_url = "-".join(nombre_limpio.split())

        if cola_url == "ciencias-juridicas-basicas":
            cola_url = "ciencias-juridicas-basicas-derecho-romano-historia-del-derecho-y-derecho"

        return cola_url

    @staticmethod
    def _asignar_facultad(departamento: Departamento, nombre_sede: str, registro: dict):
        if nombre_sede not in registro:
            registro[nombre_sede] = Facultad(nombre_sede)
        registro[nombre_sede].agregar_departamento(departamento)

    @classmethod
    def construir_facultades(cls, lista_departamentos: list) -> list:
        """Hace scraping y devuelve una LISTA de objetos Facultad ensamblados."""
        registro_facultades_por_nombre = {}
        url_base = "https://www.us.es/centros/departamentos/"
        departamentos_fallidos = []
        
        print(f"Iniciando scraping para {len(lista_departamentos)} departamentos. Esto tomará un tiempo...\n")
        
        sesion = requests.Session()
        sesion.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

        # ==========================================
        # PRIMERA PASADA (Intento normal)
        # ==========================================
        for depto in lista_departamentos:
            url_completa = url_base + cls._normalizar_nombre(depto.nombre)
            
            # ¡Aquí restauramos el print que querías!
            print(f" -> Consultando: {url_completa}")
            
            exito = False
            nombre_sede = None
            
            try:
                respuesta = sesion.get(url_completa, timeout=10)
                if respuesta.status_code == 200:
                    sopa = BeautifulSoup(respuesta.text, 'lxml') 
                    etiqueta_sede = sopa.find('h3', string='Sede')
                    if etiqueta_sede and etiqueta_sede.find_next('a'):
                        nombre_sede = etiqueta_sede.find_next('a').text.strip()
                    else:
                        nombre_sede = "Sede Desconocida"
                    exito = True
                else:
                    print(f"    [!] Error {respuesta.status_code}. Guardando en la cola de reintentos...")
            except requests.RequestException as e:
                print(f"    [!] Fallo de red: {e}. Guardando en la cola de reintentos...")

            if exito and nombre_sede:
                cls._asignar_facultad(depto, nombre_sede, registro_facultades_por_nombre)
            else:
                departamentos_fallidos.append((depto, url_completa))

        # ==========================================
        # SEGUNDA PASADA (Reintento de fallidos)
        # ==========================================
        if departamentos_fallidos:
            print(f"\n=======================================================")
            print(f"🔄 INICIANDO REINTENTO PARA {len(departamentos_fallidos)} DEPARTAMENTOS FALLIDOS")
            print(f"=======================================================")
            time.sleep(2) 
            
            for depto, url_completa in departamentos_fallidos:
                # Print también para el reintento
                print(f" -> Reintentando: {url_completa}")
                nombre_sede = "Sede Desconocida" 
                
                try:
                    respuesta = sesion.get(url_completa, timeout=15)
                    if respuesta.status_code == 200:
                        sopa = BeautifulSoup(respuesta.text, 'lxml')
                        etiqueta_sede = sopa.find('h3', string='Sede')
                        if etiqueta_sede and etiqueta_sede.find_next('a'):
                            nombre_sede = etiqueta_sede.find_next('a').text.strip()
                        print(f"    ✅ Éxito en el reintento: Sede asignada a '{nombre_sede}'")
                    else:
                        print(f"    ❌ Fallo definitivo (Error {respuesta.status_code}). Se asignará a 'Sede Desconocida'.")
                except requests.RequestException as e:
                    print(f"    ❌ Fallo definitivo de red: {e}. Se asignará a 'Sede Desconocida'.")
                    
                cls._asignar_facultad(depto, nombre_sede, registro_facultades_por_nombre)

        sesion.close()
        
        # Devolvemos directamente la lista de las Facultades extraídas del diccionario
        return list(registro_facultades_por_nombre.values())