import os
import pdfplumber

# ==========================================
# 1. CLASE DEPARTAMENTO
# ==========================================
class Departamento:
    """Clase que representa un departamento de la Universidad."""
    
    def __init__(self, nombre: str, numero_etc: float, prof_tc: float, prof_tp: float, experimentalidad: float, total_pdf: float = None):
        self.nombre = nombre
        self.numero_etc = numero_etc
        self.prof_tc = prof_tc
        self.prof_tp = prof_tp
        self.experimentalidad = experimentalidad
        
        # 1. El objeto calcula el total de profesores internamente al nacer
        self.total_profesores = self._calcular_total_profesores()
        
        # 2. El objeto calcula y guarda su carga docente como atributo desde el primer momento
        self.carga_docente_real = self._calcular_carga_docente_real()
        
        # 3. Auditoría del PDF: comprueba si la matemática cuadra con los datos leídos
        if total_pdf is not None:
            self._validar_integridad(total_pdf)

    def _calcular_total_profesores(self) -> float:
        """Calcula el número total de profesores (TC + 1/2 * TP). Método privado."""
        return self.prof_tc + (0.5 * self.prof_tp)

    def _calcular_carga_docente_real(self) -> float:
        """Calcula la carga docente real basada en la fórmula del enunciado. Método privado."""
        if self.total_profesores == 0:
            return 0.0
        return (self.numero_etc * self.experimentalidad) / self.total_profesores

    def _validar_integridad(self, total_pdf: float):
        """Comprueba que el cálculo interno coincida con el dato extraído del PDF."""
        # Redondeamos a 2 decimales para evitar desajustes de precisión al sumar flotantes
        if round(self.total_profesores, 2) != round(total_pdf, 2):
            print(f"⚠️ AVISO: Para el departamento '{self.nombre}', el total calculado ({self.total_profesores}) no coincide con el del PDF ({total_pdf}).")

    def __str__(self) -> str:
            # Formateamos el texto para que quede alineado y fácil de leer en consola
            return (f"Depto: {self.nombre:<75} | "
                    f"ETC: {self.numero_etc:<7} | "
                    f"Prof TC: {self.prof_tc:<5} | "
                    f"Prof TP: {self.prof_tp:<5} | "
                    f"Total Prof: {self.total_profesores:<6} | "
                    f"Exp: {self.experimentalidad:<4} | "
                    f"Carga Real: {self.carga_docente_real:.2f}")
    


# ==========================================
# 2. CLASE UNIVERSIDAD (Actualizada)
# ==========================================
class Universidad:
    """Clase que representa una Universidad y gestiona sus departamentos."""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.departamentos = []

    def agregar_departamento(self, departamento: Departamento):
        """Añade un objeto Departamento a la lista."""
        if isinstance(departamento, Departamento):
            self.departamentos.append(departamento)
        else:
            raise TypeError("El objeto a insertar debe ser estrictamente de la clase Departamento")

    def mostrar_resumen(self):
        """Muestra por consola la información de todos los departamentos registrados."""
        print(f"\n{'='*100}")
        print(f"--- Departamentos de la {self.nombre} ---")
        print(f"{'='*100}")
        if not self.departamentos:
            print("No hay departamentos registrados aún.")
        else:
            for depto in self.departamentos:
                print(depto)
            print(f"\nTotal de departamentos cargados: {len(self.departamentos)}")

    # --- NUEVOS MÉTODOS DE CONSULTA ---

    def top_n_mayor_carga(self, n: int) -> list:
        """1. Devuelve los 'n' departamentos con MAYOR carga docente real."""
        # Ordenamos de mayor a menor (reverse=True) usando la carga docente real como criterio
        ordenados = sorted(self.departamentos, key=lambda d: d.carga_docente_real, reverse=True)
        return ordenados[:n]

    def top_n_menor_carga(self, n: int) -> list:
        """2. Devuelve los 'n' departamentos con MENOR carga docente real."""
        # Ordenamos de menor a mayor (por defecto)
        ordenados = sorted(self.departamentos, key=lambda d: d.carga_docente_real)
        return ordenados[:n]

    def contar_por_experimentalidad(self) -> dict:
        """3. Devuelve un diccionario con el número de departamentos por cada coeficiente."""
        conteo = {}
        for depto in self.departamentos:
            coef = depto.experimentalidad
            # Si el coeficiente ya está en el diccionario le sumamos 1, si no, lo inicializamos en 1
            conteo[coef] = conteo.get(coef, 0) + 1
        return conteo

    def media_carga_por_experimentalidad(self) -> dict:
        """4. Devuelve un diccionario con la media de la carga docente por coeficiente."""
        suma_cargas = {}
        conteo = self.contar_por_experimentalidad() # Reutilizamos el método anterior
        
        # Sumamos todas las cargas docentes agrupándolas por coeficiente
        for depto in self.departamentos:
            coef = depto.experimentalidad
            suma_cargas[coef] = suma_cargas.get(coef, 0.0) + depto.carga_docente_real
            
        # Calculamos la media dividiendo la suma total entre el conteo
        medias = {}
        for coef in suma_cargas:
            medias[coef] = suma_cargas[coef] / conteo[coef]
            
        return medias

    def extremos_media_experimentalidad(self) -> tuple:
        """
        5. Usando el método anterior, devuelve una tupla con los coeficientes 
        de experimentalidad con (mayor media, menor media).
        """
        medias = self.media_carga_por_experimentalidad()
        if not medias:
            return None, None
            
        # Encontramos la clave (el coeficiente) que tiene el valor máximo y mínimo en el diccionario
        coef_mayor_media = max(medias, key=medias.get)
        coef_menor_media = min(medias, key=medias.get)
        
        return coef_mayor_media, coef_menor_media


# ==========================================
# 3. CLASE FACTORÍA (Gestión de lectura)
# ==========================================
class FactoriaUniversidad:
    """Clase Factoría encargada de leer fuentes de datos y construir objetos Universidad."""

    @staticmethod
    def _limpiar_numero(texto: str) -> float:
        """Limpia las cadenas de texto del PDF para convertirlas en números flotantes."""
        if not texto:
            return 0.0
        
        texto = str(texto).strip()
        if texto == "" or texto == "-":
            return 0.0
            
        # Limpiamos el formato numérico español (1.479,36 -> 1479.36)
        texto = texto.replace('.', '').replace(',', '.')
        
        try:
            return float(texto)
        except ValueError:
            return 0.0

    @classmethod
    def leer_pdf(cls, ruta_pdf: str, nombre_uni: str) -> Universidad:
        """Lee el PDF, extrae y limpia los datos, y construye la Universidad."""
        universidad = Universidad(nombre_uni)
        
        with pdfplumber.open(ruta_pdf) as pdf:
            for pagina in pdf.pages:
                tablas = pagina.extract_tables()
                for tabla in tablas:
                    for fila in tabla:
                        # 1. Si la fila está vacía, la saltamos
                        if not fila or not fila[0]:
                            continue
                        
                        # 2. Extraemos el texto crudo del primer (y único) elemento
                        texto_fila = str(fila[0]).strip()
                        
                        # 3. Verificamos que sea realmente una línea de departamento válida
                        if not texto_fila.upper().startswith("DEPARTAMENTO"):
                            continue
                        
                        try:
                            # 4. Dividimos la línea por los espacios
                            elementos = texto_fila.split()
                            
                            # Necesitamos al menos el nombre (1 palabra) + 5 números = 6 elementos
                            if len(elementos) < 6:
                                continue
                            
                            # 5. Los 5 últimos elementos siempre son los números (leídos de derecha a izquierda)
                            experimentalidad = cls._limpiar_numero(elementos[-1])
                            total_pdf = cls._limpiar_numero(elementos[-2])
                            tp = cls._limpiar_numero(elementos[-3])
                            tc = cls._limpiar_numero(elementos[-4])
                            etc = cls._limpiar_numero(elementos[-5])
                            
                            # 6. Todo lo que está antes de los 5 números es el nombre del departamento
                            nombre = " ".join(elementos[:-5]).strip()
                            
                            # 7. Fabricamos el objeto
                            nuevo_depto = Departamento(
                                nombre=nombre,
                                numero_etc=etc,
                                prof_tc=tc,
                                prof_tp=tp,
                                experimentalidad=experimentalidad,
                                total_pdf=total_pdf
                            )
                            
                            # 8. Lo añadimos a la lista de la universidad
                            universidad.agregar_departamento(nuevo_depto)
                            
                        except Exception as e:
                            print(f"Error procesando la línea '{texto_fila}': {e}")
                            
        return universidad


# ==========================================
# 4. BLOQUE PRINCIPAL DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    # 1. Obtenemos la ruta dinámica de la carpeta donde está este script
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Unimos la ruta con el nombre del archivo PDF de forma segura
    archivo_pdf = os.path.join(directorio_actual, "departamentos.pdf")
    
    # 3. Usamos nuestra Factoría para construir la universidad
    print("Iniciando la lectura y creación de objetos. Por favor, espera...")
    uni_sevilla = FactoriaUniversidad.leer_pdf(archivo_pdf, "Universidad de Sevilla")
    
    # 4. Mostramos el resultado final
    uni_sevilla.mostrar_resumen()

    print(uni_sevilla.contar_por_experimentalidad)

    print(uni_sevilla.extremos_media_experimentalidad)

    print(uni_sevilla.media_carga_por_experimentalidad)
