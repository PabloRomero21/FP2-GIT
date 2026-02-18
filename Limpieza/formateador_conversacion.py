import re
import os

def formatear_conversacion(archivo_entrada: str, archivo_salida: str):
    """
    Lee el archivo en bruto de la conversación, lo formatea con separadores 
    elegantes y lo guarda en un nuevo archivo Markdown.
    """
    try:
        # 1. Leer el texto original
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            texto = f.read()

        # 2. Formatear las intervenciones del estudiante
        # Buscamos "Has dicho" y lo cambiamos por un encabezado claro
        texto = re.sub(
            r'\bHas dicho\b', 
            r'\n\n---\n\n### 👤 Tú (Estudiante):\n> ', 
            texto
        )

        # 3. Formatear las intervenciones de la IA
        # Buscamos el bloque exacto que genera tu Gem personalizado (soporta saltos de línea variables)
        patron_ia = r'FP2\s*Gem personalizado\s*FP2 said'
        texto = re.sub(
            patron_ia, 
            r'\n\n### 🤖 FP2 (Asistente POO):\n', 
            texto
        )

        # 4. Limpieza estética (quitar saltos de línea excesivos que afean el documento)
        texto = re.sub(r'\n{4,}', r'\n\n', texto)

        # 5. Escribir el resultado con un título de presentación
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write("# 🎓 Registro de Tutoría y Desarrollo de Código\n")
            f.write("*Conversación de asistencia para la práctica de Programación Orientada a Objetos.*\n\n")
            f.write(texto)

        print(f"✅ ¡Éxito! Conversación formateada y guardada en '{archivo_salida}'")

    except FileNotFoundError:
        print(f"❌ Error: No se ha encontrado el archivo '{archivo_entrada}'.")
    except Exception as e:
        print(f"⚠️ Ocurrió un error inesperado: {e}")

# ==========================================
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    # Nombres de tus archivos
    archivo_bruto = "conversacion_bruta.txt"
    archivo_limpio = "entrega_profesor.md"
    
    # Obtenemos la ruta absoluta (¡aplicando lo que aprendiste en tu práctica!)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_entrada = os.path.join(directorio_actual, archivo_bruto)
    ruta_salida = os.path.join(directorio_actual, archivo_limpio)
    
    formatear_conversacion(ruta_entrada, ruta_salida)