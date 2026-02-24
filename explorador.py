import requests
from bs4 import BeautifulSoup

def ver_que_ve_python():
    """Script exploratorio para extraer la sede de un departamento concreto."""
    
    url = "https://www.us.es/centros/departamentos/administracion-de-empresas-y-marketing"
    
    print(f"Haciendo la petición a: {url}...")
    
    # 1. Realizamos la petición HTTP GET
    respuesta = requests.get(url)
    
    # 2. Verificamos que la página existe (Código 200)
    if respuesta.status_code == 200:
        print("✅ ¡Conexión exitosa! Analizando el HTML...\n")
        
        # 3. Pasamos el texto HTML a BeautifulSoup
        sopa = BeautifulSoup(respuesta.text, 'html.parser')
        
        print("=== EXTRACCIÓN PRECISA DE LA SEDE ===")
        
        # 4. Buscamos la etiqueta <h3> que contiene exactamente el texto "Sede"
        etiqueta_sede = sopa.find('h3', string='Sede')
        
        if etiqueta_sede:
            # 5. Buscamos el primer enlace (etiqueta <a>) que aparezca DESPUÉS de ese <h3>
            enlace_facultad = etiqueta_sede.find_next('a')
            
            if enlace_facultad:
                # Extraemos el texto limpio
                nombre_facultad = enlace_facultad.text.strip()
                print(f"✅ Sede extraída con éxito: {nombre_facultad}")
            else:
                print("❌ Se encontró 'Sede', pero no había ningún enlace con el nombre de la facultad.")
        else:
            print("❌ No se encontró la etiqueta <h3>Sede</h3> en esta página.")
                
    else:
        print(f"❌ Error al conectar. Código: {respuesta.status_code}")

if __name__ == "__main__":
    ver_que_ve_python()