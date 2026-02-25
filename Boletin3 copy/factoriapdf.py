# factoria.py
import pdfplumber
from departamento import Departamento

class Factoriapdf:
    """Factoría que lee el PDF y fabrica los objetos Departamento base."""

    @staticmethod
    def _limpiar_numero(texto: str) -> float:
        if not texto: return 0.0
        texto = str(texto).strip()
        if texto in ("", "-"): return 0.0
        if ',' in texto:
            texto = texto.replace('.', '').replace(',', '.')
        try: return float(texto)
        except ValueError: return 0.0

    @classmethod
    def extraer_departamentos_pdf(cls, ruta_pdf: str) -> list:
        """Devuelve una lista plana con los objetos Departamento extraídos del PDF."""
        lista_deptos = []
        
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
                            
                            if nuevo_depto.es_integro(total_pdf):
                                lista_deptos.append(nuevo_depto) 
                                
                        except Exception as e:
                            print(f"Error parseando la línea '{texto_fila}': {e}")
                            
        return lista_deptos