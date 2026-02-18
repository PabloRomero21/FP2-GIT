# factoria.py
import pdfplumber
from departamento import Departamento
from universidad import Universidad

class FactoriaUniversidad:
    """Clase Factoría que maneja la entrada/salida (I/O) y la construcción de objetos."""

    @staticmethod
    def _limpiar_numero(texto: str) -> float:
        if not texto: return 0.0
        texto = str(texto).strip()
        if texto in ("", "-"): return 0.0
        texto = texto.replace('.', '').replace(',', '.')
        try: return float(texto)
        except ValueError: return 0.0

    @classmethod
    def leer_pdf(cls, ruta_pdf: str, nombre_uni: str) -> Universidad:
        universidad = Universidad(nombre_uni)
        
        with pdfplumber.open(ruta_pdf) as pdf:
            for pagina in pdf.pages:
                for tabla in pagina.extract_tables():
                    for fila in tabla:
                        columnas_validas = [str(col).strip() for col in fila if col is not None and str(col).strip()]
                        texto_fila = " ".join(columnas_validas)
                        
                        if not texto_fila.upper().startswith("DEPARTAMENTO"):
                            continue
                        
                        try:
                            elementos = texto_fila.split()
                            if len(elementos) < 6:
                                continue
                            
                            exp = cls._limpiar_numero(elementos[-1])
                            total_pdf = cls._limpiar_numero(elementos[-2])
                            tp = cls._limpiar_numero(elementos[-3])
                            tc = cls._limpiar_numero(elementos[-4])
                            etc = cls._limpiar_numero(elementos[-5])
                            nombre = " ".join(elementos[:-5]).strip()
                            
                            nuevo_depto = Departamento(nombre, etc, tc, tp, exp)
                            
                            if not nuevo_depto.es_integro(total_pdf):
                                print(f"⚠️ AVISO LECTURA: Los datos de '{nombre}' están corruptos en el PDF.")
                            
                            universidad.agregar_departamento(nuevo_depto)
                            
                        except Exception as e:
                            print(f"Error parseando la línea '{texto_fila}': {e}")
                            
        return universidad