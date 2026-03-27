# Importamos las clases creadas anteriormente (asumiendo que están en proyectos.py)
from proyectos import ProyectoContrato # Asegúrate de tener esto importado arriba del archivo
from proyectos import Proyecto, ProyectoConcedido, ProyectoContrato
from diccionario_aei import obtener_mapa_subareas

class Gestor_Proyectos:
    """
    Contenedor general para TODOS los proyectos (tanto concedidos como denegados).
    """
    def __init__(self):
        # Inicializamos el diccionario vacío. 
        # Clave: referencia (str) -> Valor: objeto Proyecto
        self.proyectos: dict[str, Proyecto] = {}
        self.poblacion_ccaa = {}

    def agregar_proyecto(self, proyecto: Proyecto):
        """Añade un proyecto al diccionario usando su referencia como clave."""
        self.proyectos[proyecto.referencia] = proyecto

    def agregar_poblacion(self, ccaa: str, habitantes: int):
        self.poblacion_ccaa[ccaa] = habitantes

    def obtener_total(self) -> int:
        """Devuelve el número total de proyectos almacenados."""
        return len(self.proyectos)
    
    def calcular_tasas_exito_ccaa(self) -> dict:
        """
        Calcula internamente las estadísticas y devuelve un diccionario
        con los datos crudos listos para ser mostrados por la interfaz.
        """
        estadisticas = {}

        for proyecto in self.proyectos.values():
            ccaa = proyecto.comunidad_autonoma
            if not ccaa:
                continue
                
            if ccaa not in estadisticas:
                estadisticas[ccaa] = {'solicitados': 0, 'concedidos': 0, 'contratos': 0}
                
            estadisticas[ccaa]['solicitados'] += 1
            
            if proyecto.concedido:
                estadisticas[ccaa]['concedidos'] += 1
                
            if isinstance(proyecto, ProyectoContrato):
                estadisticas[ccaa]['contratos'] += 1
                
        # Podemos incluso calcular los porcentajes aquí mismo antes de devolverlo
        for ccaa, datos in estadisticas.items():
            if datos['solicitados'] > 0:
                datos['tasa_concedidos'] = (datos['concedidos'] / datos['solicitados']) * 100
                datos['tasa_contratos'] = (datos['contratos'] / datos['solicitados']) * 100
            else:
                datos['tasa_concedidos'] = 0.0
                datos['tasa_contratos'] = 0.0

        return estadisticas
    

    def calcular_financiacion_por_habitante(self) -> dict:
        """
        Cruza los datos internos de presupuestos y población
        y devuelve la ratio de € / habitante por cada CCAA.
        """
        # 1. Calcular el presupuesto total CONCEDIDO por Comunidad Autónoma
        presupuesto_por_ccaa = {}
        for proyecto in self.proyectos.values():
            if proyecto.concedido:
                ccaa = proyecto.comunidad_autonoma.strip().upper()
                if not ccaa: continue
                
                if ccaa not in presupuesto_por_ccaa:
                    presupuesto_por_ccaa[ccaa] = 0.0
                presupuesto_por_ccaa[ccaa] += proyecto.presupuesto

        # 2. Cruzar datos y calcular la Tasa usando el diccionario interno self.poblacion_ccaa
        resultados = {}
        for ccaa, presupuesto in presupuesto_por_ccaa.items():
            # Recuperamos los habitantes (si no existe la CCAA en el diccionario, devuelve 0)
            habitantes = self.poblacion_ccaa.get(ccaa, 0)
            
            if habitantes > 0:
                tasa = presupuesto / habitantes
                resultados[ccaa] = {
                    'presupuesto': presupuesto,
                    'habitantes': habitantes,
                    'tasa_per_capita': tasa
                }
            else:
                resultados[ccaa] = {
                    'presupuesto': presupuesto,
                    'habitantes': 0,
                    'tasa_per_capita': 0.0,
                    'error': 'Falta dato de población'
                }
                
        return resultados
    
    def obtener_top_n_entidades_exito(self, n: int) -> tuple[list, list]:
        """
        Calcula la tasa de éxito por entidad y devuelve dos listas:
        el Top N de concedidos y el Top N de contratos.
        """

        estadisticas = {}

        # 1. Agrupamos y contamos todos los proyectos por Entidad
        for proyecto in self.proyectos.values():
            # ¡OJO AQUÍ! Cambia '.entidad' por el nombre real de tu atributo si es distinto
            nombre_entidad = proyecto.entidad_solicitante
            
            if not nombre_entidad:
                continue
                
            if nombre_entidad not in estadisticas:
                estadisticas[nombre_entidad] = {'solicitados': 0, 'concedidos': 0, 'contratos': 0}
                
            estadisticas[nombre_entidad]['solicitados'] += 1
            
            if proyecto.concedido:
                estadisticas[nombre_entidad]['concedidos'] += 1
                
            if isinstance(proyecto, ProyectoContrato):
                estadisticas[nombre_entidad]['contratos'] += 1

        # 2. Calculamos las tasas y lo pasamos a una lista para poder ordenarlo
        lista_tasas = []
        for entidad, datos in estadisticas.items():
            if datos['solicitados'] > 0:
                tasa_conc = (datos['concedidos'] / datos['solicitados']) * 100
                tasa_cont = (datos['contratos'] / datos['solicitados']) * 100
                
                lista_tasas.append({
                    'entidad': entidad,
                    'solicitados': datos['solicitados'],
                    'concedidos': datos['concedidos'],
                    'tasa_concedidos': tasa_conc,
                    'contratos': datos['contratos'],
                    'tasa_contratos': tasa_cont
                })

        # 3. Ordenamos de mayor a menor (reverse=True) usando una función lambda
        # y cortamos la lista hasta el elemento 'n' usando slicing [:n]
        top_concedidos = sorted(lista_tasas, key=lambda x: x['tasa_concedidos'], reverse=True)[:n]
        top_contratos = sorted(lista_tasas, key=lambda x: x['tasa_contratos'], reverse=True)[:n]

        # Devolvemos ambas listas
        return top_concedidos, top_contratos
    

    # Al principio de gestor.py, asegúrate de importar el mapa


    def calcular_estadisticas_por_nivel(self, nivel_agrupacion="area") -> dict:
        """
        nivel_agrupacion puede ser "area" o "macroarea".
        Cruza la subárea del proyecto con el diccionario AEI y calcula las tasas.
        """
        from proyectos import ProyectoContrato
        from diccionario_aei import obtener_mapa_subareas
        
        mapa_aei = obtener_mapa_subareas()
        estadisticas = {}
        
        # ¡AQUÍ! 1. Inicializamos la "caja" vacía donde guardaremos las raras
        subareas_desconocidas = set() 

        for proyecto in self.proyectos.values():
            # Asumo que en tu clase Proyecto la variable se llama 'area' (que realmente guarda la subárea)
            subarea_excel = proyecto.area.strip().upper() if proyecto.area else ""
            
            if not subarea_excel: continue

            # Buscamos a qué Área y Macroárea pertenece esa subárea
            info_jerarquia = mapa_aei.get(subarea_excel)
            
            if info_jerarquia:
                # Elegimos la etiqueta por la que vamos a agrupar
                etiqueta = info_jerarquia[nivel_agrupacion] 
            else:
                etiqueta = "OTROS / SIN CLASIFICAR"
                # ¡AQUÍ! 2. Si no la reconoce, la metemos en nuestra "caja"
                subareas_desconocidas.add(subarea_excel)

            # Agrupamos los conteos
            if etiqueta not in estadisticas:
                estadisticas[etiqueta] = {'solicitados': 0, 'concedidos': 0, 'contratos': 0}
                
            estadisticas[etiqueta]['solicitados'] += 1
            if proyecto.concedido:
                estadisticas[etiqueta]['concedidos'] += 1
            if isinstance(proyecto, ProyectoContrato):
                estadisticas[etiqueta]['contratos'] += 1
        
        # 3. Al terminar el bucle, imprimimos todo lo que hay en la "caja"
        if subareas_desconocidas:
            print(f"\n⚠️ AVISO: Hay {len(subareas_desconocidas)} nombres de subáreas en el Excel que no están en el diccionario:")
            print(subareas_desconocidas)
            print("-" * 50)

        # Calculamos los porcentajes finales
        resultados = {}
        for clave, datos in estadisticas.items():
            solic = datos['solicitados']
            if solic > 0:
                resultados[clave] = {
                    'solicitados': solic,
                    'concedidos': datos['concedidos'],
                    'tasa_concedidos': (datos['concedidos'] / solic) * 100,
                    'contratos': datos['contratos'],
                    'tasa_contratos': (datos['contratos'] / solic) * 100
                }
        return resultados

    # Funciones "envoltorio" para que sea más fácil llamarlas desde el Main
    def obtener_tasa_exito_por_area(self) -> dict:
        return self.calcular_estadisticas_por_nivel(nivel_agrupacion="area")

    def obtener_tasa_exito_por_macroarea(self) -> dict:
        return self.calcular_estadisticas_por_nivel(nivel_agrupacion="macroarea")


class Gestor_ProyectosConcedidos:
    """
    Contenedor exclusivo para los proyectos que han sido concedidos.
    """
    def __init__(self):
        # Clave: referencia (str) -> Valor: objeto ProyectoConcedido
        self.proyectos_concedidos: dict[str, ProyectoConcedido] = {}

    def agregar_proyecto(self, proyecto: ProyectoConcedido):
        self.proyectos_concedidos[proyecto.referencia] = proyecto

    def obtener_total(self) -> int:
        return len(self.proyectos_concedidos)


class Gestor_ProyectosContrato:
    """
    Contenedor exclusivo para los proyectos concedidos con contrato predoctoral.
    """
    def __init__(self):
        # Clave: referencia (str) -> Valor: objeto ProyectoContrato
        self.proyectos_contrato: dict[str, ProyectoContrato] = {}

    def agregar_proyecto(self, proyecto: ProyectoContrato):
        self.proyectos_contrato[proyecto.referencia] = proyecto

    def obtener_total(self) -> int:
        return len(self.proyectos_contrato)