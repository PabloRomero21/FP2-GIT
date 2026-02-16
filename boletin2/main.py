import os
import pdfplumber

# ==========================================
# 1. CLASE DEPARTAMENTO
# ==========================================
class Departamento:
    """Clase de dominio que representa un departamento de la Universidad."""
    
    def __init__(self, nombre: str, numero_etc: float, prof_tc: float, prof_tp: float, experimentalidad: float):
        self.nombre = nombre
        self.numero_etc = numero_etc
        self.prof_tc = prof_tc
        self.prof_tp = prof_tp
        self.experimentalidad = experimentalidad

    @property
    def total_profesores(self) -> float:
        """Atributo derivado: Calcula el total de profesores en tiempo real."""
        return self.prof_tc + (0.5 * self.prof_tp)

    @property
    def carga_docente_real(self) -> float:
        """Atributo derivado: Calcula la carga docente en tiempo real."""
        if self.total_profesores == 0:
            return float('inf')  # Conceptualmente, 0 profesores implica carga infinita
        return (self.numero_etc * self.experimentalidad) / self.total_profesores

    def es_integro(self, total_pdf: float) -> bool:
        """
        Devuelve True si el cálculo coincide con el PDF, False si no.
        Cumple SRP: No hace prints, solo devuelve el estado lógico.
        """
        return round(self.total_profesores, 2) == round(total_pdf, 2)

    def __str__(self) -> str:
        # Manejo estético por si la carga es infinita
        carga_str = "Infinita" if self.carga_docente_real == float('inf') else f"{self.carga_docente_real:.2f}"
        return f"Depto: {self.nombre:<75} | Total Prof: {self.total_profesores:<6} | Carga Real: {carga_str}"


# ==========================================
# 2. CLASE UNIVERSIDAD
# ==========================================
class Universidad:
    """Clase que gestiona la colección de departamentos y la lógica de negocio."""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.departamentos = []

    def agregar_departamento(self, departamento: Departamento):
        if isinstance(departamento, Departamento):
            self.departamentos.append(departamento)
        else:
            raise TypeError("El objeto a insertar debe ser de la clase Departamento")

    # --- RESPUESTAS AL ENUNCIADO ---

    def top_n_mayor_carga(self, n: int) -> list:
        """1. Dado n, cuáles son los n departamentos con MAYOR carga docente real."""
        return sorted(self.departamentos, key=lambda d: d.carga_docente_real, reverse=True)[:n]

    def top_n_menor_carga(self, n: int) -> list:
        """2. Dado n, cuáles son los n departamentos con MENOR carga docente real."""
        return sorted(self.departamentos, key=lambda d: d.carga_docente_real)[:n]

    def contar_por_experimentalidad(self) -> dict:
        """3. Devuelve un diccionario con el número de departamentos de cada coeficiente."""
        conteo = {}
        for depto in self.departamentos:
            coef = depto.experimentalidad
            conteo[coef] = conteo.get(coef, 0) + 1
        return conteo

    def media_carga_por_experimentalidad(self) -> dict:
        """4. Devuelve un diccionario con la media de la carga docente por coeficiente."""
        suma_cargas = {}
        conteo = self.contar_por_experimentalidad()
        
        for depto in self.departamentos:
            coef = depto.experimentalidad
            # Ignoramos cargas infinitas para no romper la media matemática
            if depto.carga_docente_real != float('inf'):
                suma_cargas[coef] = suma_cargas.get(coef, 0.0) + depto.carga_docente_real
            
        return {coef: suma_cargas[coef] / conteo[coef] for coef in suma_cargas}

    def extremos_media_experimentalidad(self) -> tuple:
        """5. Devuelve los coeficientes con mayor y menor media de carga docente real."""
        medias = self.media_carga_por_experimentalidad()
        if not medias:
            return None, None
            
        coef_mayor = max(medias, key=medias.get)
        coef_menor = min(medias, key=medias.get)
        return coef_mayor, coef_menor


# ==========================================
# 3. CLASE FACTORÍA
# ==========================================
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
                        # 1. SOLUCIÓN FALLO CRÍTICO: Aplanamos toda la fila de forma segura
                        columnas_validas = [str(col).strip() for col in fila if col is not None and str(col).strip()]
                        texto_fila = " ".join(columnas_validas)
                        
                        if not texto_fila.upper().startswith("DEPARTAMENTO"):
                            continue
                        
                        try:
                            elementos = texto_fila.split()
                            if len(elementos) < 6:
                                continue
                            
                            # Extraemos datos
                            exp = cls._limpiar_numero(elementos[-1])
                            total_pdf = cls._limpiar_numero(elementos[-2])
                            tp = cls._limpiar_numero(elementos[-3])
                            tc = cls._limpiar_numero(elementos[-4])
                            etc = cls._limpiar_numero(elementos[-5])
                            nombre = " ".join(elementos[:-5]).strip()
                            
                            # Construimos el objeto
                            nuevo_depto = Departamento(nombre, etc, tc, tp, exp)
                            
                            # SOLUCIÓN SRP: La factoría hace el print, el objeto solo devuelve True/False
                            if not nuevo_depto.es_integro(total_pdf):
                                print(f"⚠️ AVISO LECTURA: Los datos de '{nombre}' están corruptos en el PDF.")
                            
                            universidad.agregar_departamento(nuevo_depto)
                            
                        except Exception as e:
                            print(f"Error parseando la línea '{texto_fila}': {e}")
                            
        return universidad


# ==========================================
# 4. BLOQUE PRINCIPAL
# ==========================================
if __name__ == "__main__":
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_pdf = os.path.join(directorio_actual, "departamentos.pdf")
    
    print("Iniciando la lectura del PDF...")
    uni = FactoriaUniversidad.leer_pdf(archivo_pdf, "Universidad de Sevilla")
    
    # RESPUESTAS AL ENUNCIADO
    N = 3 # Puedes cambiar este valor
    
    print(f"\n--- 1. TOP {N} DEPARTAMENTOS CON MAYOR CARGA DOCENTE ---")
    for d in uni.top_n_mayor_carga(N):
        print(f"{d.nombre} -> {d.carga_docente_real:.2f}")

    print(f"\n--- 2. TOP {N} DEPARTAMENTOS CON MENOR CARGA DOCENTE ---")
    for d in uni.top_n_menor_carga(N):
        print(f"{d.nombre} -> {d.carga_docente_real:.2f}")

    print("\n--- 3. DEPARTAMENTOS POR COEFICIENTE DE EXPERIMENTALIDAD ---")
    conteo = uni.contar_por_experimentalidad()
    for coef, cant in sorted(conteo.items()):
        print(f"Coeficiente {coef}: {cant} departamentos")

    print("\n--- 4. MEDIA DE CARGA DOCENTE POR COEFICIENTE ---")
    medias = uni.media_carga_por_experimentalidad()
    for coef, media in sorted(medias.items()):
        print(f"Coeficiente {coef}: {media:.2f} de media")

    print("\n--- 5. EXTREMOS DE MEDIAS POR EXPERIMENTALIDAD ---")
    mayor, menor = uni.extremos_media_experimentalidad()
    if mayor and menor:
        print(f"MAYOR media: Coeficiente {mayor} (Media: {medias[mayor]:.2f})")
        print(f"MENOR media: Coeficiente {menor} (Media: {medias[menor]:.2f})")