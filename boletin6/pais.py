import matplotlib.pyplot as plt

class Pais:
    def __init__(self, nombre, lista_comunidades=None, lista_partidos=None):
        self.nombre = nombre
        
        # Diccionario de Comunidades Autónomas
        # Clave: ID o Nombre -> Valor: Objeto ComunidadAutonoma
        self.comunidades_autonomas = {}
        if lista_comunidades is not None:
            for clave_comunidad, objeto_comunidad in lista_comunidades:
                self.comunidades_autonomas[clave_comunidad] = objeto_comunidad
                
        # Diccionario de Partidos Políticos
        # Clave: Nombre del Partido -> Valor: Objeto Partido
        self.partidos = {}
        if lista_partidos is not None:
            for nombre_partido, objeto_partido in lista_partidos:
                self.partidos[nombre_partido] = objeto_partido


    def graficar_resultados(self, nivel="nacional", id_comunidad=None, id_provincia=None):
        """
        Representa gráficamente los resultados electorales mediante 
        un diagrama de sectores (quesito) y un diagrama de barras.
        Niveles permitidos: 'nacional', 'comunidad', 'provincial'
        """
        votos_por_partido = {}
        titulo = ""

        # 1. RECOLECCIÓN DE DATOS SEGÚN EL NIVEL
        if nivel == "nacional":
            titulo = f"Resultados Nacionales - {self.nombre}"
            # Recorremos todas las comunidades y sus provincias
            for comunidad in self.comunidades_autonomas.values():
                for provincia in comunidad.provincias.values():
                    for partido, (votos, diputados) in provincia.resultados_partidos.items():
                        votos_por_partido[partido] = votos_por_partido.get(partido, 0) + votos

        elif nivel == "comunidad":
            if id_comunidad not in self.comunidades_autonomas:
                print(f"Error: La comunidad '{id_comunidad}' no existe.")
                return
            
            comunidad = self.comunidades_autonomas[id_comunidad]
            titulo = f"Resultados Autonómicos - {comunidad.nombre}"
            
            # Recorremos solo las provincias de esta comunidad
            for provincia in comunidad.provincias.values():
                for partido, (votos, diputados) in provincia.resultados_partidos.items():
                    votos_por_partido[partido] = votos_por_partido.get(partido, 0) + votos

        elif nivel == "provincial":
            if id_comunidad not in self.comunidades_autonomas:
                print(f"Error: La comunidad '{id_comunidad}' no existe.")
                return
            
            comunidad = self.comunidades_autonomas[id_comunidad]
            provincia_objetivo = None

            # Buscamos la provincia. Primero intentamos por la clave directa (ID/Código)
            if id_provincia in comunidad.provincias:
                provincia_objetivo = comunidad.provincias[id_provincia]
            else:
                # Si no es la clave, buscamos por el atributo 'nombre' ignorando mayúsculas/minúsculas
                for prov in comunidad.provincias.values():
                    if prov.nombre.lower() == str(id_provincia).lower():
                        provincia_objetivo = prov
                        break
            
            if provincia_objetivo is None:
                print(f"Error: Provincia '{id_provincia}' no encontrada dentro de {comunidad.nombre}.")
                return
            
            titulo = f"Resultados Provinciales - {provincia_objetivo.nombre}"
            
            # Obtenemos los votos directos de la provincia
            for partido, (votos, diputados) in provincia_objetivo.resultados_partidos.items():
                votos_por_partido[partido] = votos_por_partido.get(partido, 0) + votos

        else:
            print("Nivel no válido. Usa 'nacional', 'comunidad' o 'provincial'.")
            return

        # 2. PREPARACIÓN DE DATOS (Limpieza)
        # Filtramos partidos con 0 votos para que la gráfica no sea un caos visual
        votos_limpios = {p: v for p, v in votos_por_partido.items() if v > 0}
        
        if not votos_limpios:
            print("No hay datos de votos suficientes para generar las gráficas.")
            return

        nombres_partidos = list(votos_limpios.keys())
        cantidad_votos = list(votos_limpios.values())

# 3. CREACIÓN DE LAS GRÁFICAS (Orientación a Objetos en Matplotlib)
        # Hacemos la figura un poco más alta (14, 8) para que quepa la leyenda abajo
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))

        # --- Sincronización de Colores ---
        # Usamos una paleta de colores por defecto de matplotlib ('tab20' tiene 20 colores distintos)
        paleta = plt.get_cmap('tab20').colors
        # Nos aseguramos de tener suficientes colores iterando sobre la paleta
        colores_partidos = [paleta[i % len(paleta)] for i in range(len(nombres_partidos))]

        # --- Gráfico 1: Sectores circulares (Pie Chart) ---
        wedges, texts, autotexts = ax1.pie(cantidad_votos, autopct='%1.1f%%', 
                                           startangle=90, colors=colores_partidos)
        ax1.set_title('Porcentaje de Votos')

        # --- Gráfico 2: Diagrama de Barras (Bar Chart) ---
        ax2.bar(nombres_partidos, cantidad_votos, color=colores_partidos, edgecolor='black')
        ax2.set_title('Total de Votos por Partido')
        ax2.set_ylabel('Número de Votos')
        
        # ¡Magia visual! Eliminamos por completo los textos del eje X
        ax2.set_xticks([]) 

        # --- LEYENDA GLOBAL EN LA PARTE INFERIOR ---
        # Creamos una leyenda para toda la figura (fig.legend en vez de ax.legend)
        # ncol=4 reparte los partidos en 4 columnas para que no quede una lista larguísima hacia abajo
        fig.legend(wedges, nombres_partidos, title="Partidos Políticos", 
                   loc="lower center", bbox_to_anchor=(0.5, 0.02), ncol=4, fontsize=9)

        # Ajustes finales y renderizado
        fig.suptitle(titulo, fontsize=16, fontweight='bold')
        
        # Primero ajustamos el layout general, y luego hacemos un "hueco" explícito 
        # en la parte inferior (bottom=0.25) reservando el 25% de la ventana para la leyenda.
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.25) 
        plt.show()

    def ranking_votos_nulos_blancos(self):
        """
        Busca y devuelve la Comunidad Autónoma y la Provincia con 
        el mayor porcentaje de votos nulos y en blanco.
        """
        # 1. Encontrar la Comunidad Autónoma con mayor porcentaje
        ccaa_max = max(self.comunidades_autonomas.values(), key=lambda c: c.porcentaje_nulos_blancos)

        # 2. Encontrar la Provincia con mayor porcentaje
        todas_las_provincias = []
        for comunidad in self.comunidades_autonomas.values():
            todas_las_provincias.extend(comunidad.provincias.values())

        provincia_max = max(todas_las_provincias, key=lambda p: p.porcentaje_nulos_blancos)

        # 3. Devolvemos los datos en crudo (una tupla con ambos objetos)
        return ccaa_max, provincia_max
    

    def ranking_participacion_cera(self):
        """
        Busca y devuelve la Comunidad Autónoma y la Provincia con 
        el mayor porcentaje de participación de votantes CERA.
        """
        # 1. Encontrar la Comunidad Autónoma con mayor participación
        ccaa_max = max(self.comunidades_autonomas.values(), key=lambda c: c.participacion_cera)

        # 2. Encontrar la Provincia con mayor participación
        todas_las_provincias = []
        for comunidad in self.comunidades_autonomas.values():
            todas_las_provincias.extend(comunidad.provincias.values())

        provincia_max = max(todas_las_provincias, key=lambda p: p.participacion_cera)

        # 3. Devolvemos los datos en crudo
        return ccaa_max, provincia_max
    

    def partidos_en_n_provincias(self, n):
        """
        Devuelve una lista de objetos Partido que se han presentado 
        en exactamente 'n' provincias.
        """
        # Usamos una lista por comprensión para filtrar rápidamente
        partidos_filtrados = [
            partido for partido in self.partidos.values() 
            if partido.num_provincias_presentado == n
        ]
        
        return partidos_filtrados
    

    def ccaa_mayor_proporcion_cera(self):
        """
        Busca y devuelve la Comunidad Autónoma con la mayor proporción 
        de votantes CERA respecto a su población total.
        """
        # Buscamos la CCAA usando nuestra nueva propiedad como criterio
        ccaa_max = max(self.comunidades_autonomas.values(), key=lambda c: c.proporcion_votantes_cera_poblacion)
        
        return ccaa_max
    

    def calcular_escanos_dhondt(self, id_comunidad, id_provincia):
        """
        Calcula el reparto de escaños en una provincia usando la Ley D'Hondt.
        """
        # 1. Buscar la provincia de forma robusta (como hicimos en las gráficas)
        if id_comunidad not in self.comunidades_autonomas:
            print(f"Error: La comunidad '{id_comunidad}' no existe.")
            return None
        
        comunidad = self.comunidades_autonomas[id_comunidad]
        provincia_objetivo = None

        if id_provincia in comunidad.provincias:
            provincia_objetivo = comunidad.provincias[id_provincia]
        else:
            for prov in comunidad.provincias.values():
                if prov.nombre.lower() == str(id_provincia).lower():
                    provincia_objetivo = prov
                    break
        
        if provincia_objetivo is None:
            print(f"Error: Provincia '{id_provincia}' no encontrada.")
            return None

        # 2. Recopilar datos: Votos por partido y total de escaños en juego
        votos_partidos = {}
        total_escanos_a_repartir = 0
        
        # Iteramos sobre los resultados reales para extraer los votos y averiguar los escaños totales
        for partido, (votos, diputados) in provincia_objetivo.resultados_partidos.items():
            if votos > 0:
                votos_partidos[partido] = votos
            total_escanos_a_repartir += diputados 
            
        if total_escanos_a_repartir == 0:
            print(f"No hay escaños para repartir en {provincia_objetivo.nombre}.")
            return {}

        # 3. ALGORITMO D'HONDT
        # Preparamos un diccionario con 0 escaños para cada partido
        escanos_asignados = {partido: 0 for partido in votos_partidos}
        cocientes = []

        # Calculamos todos los cocientes (Votos / Divisor)
        for partido, votos in votos_partidos.items():
            for divisor in range(1, total_escanos_a_repartir + 1):
                cociente = votos / divisor
                # Guardamos una tupla: (cociente, votos_totales, partido)
                # Los votos_totales sirven para desempatar si dos partidos tienen el mismo cociente
                cocientes.append((cociente, votos, partido))

        # Ordenamos la lista entera de cocientes de mayor a menor
        cocientes.sort(key=lambda x: (x[0], x[1]), reverse=True)

        # Repartimos los escaños cogiendo los "N" primeros de la lista
        for i in range(total_escanos_a_repartir):
            partido_ganador = cocientes[i][2]
            escanos_asignados[partido_ganador] += 1

        # 4. Limpieza de datos (quitamos a los partidos que se quedaron con 0 escaños)
        resultado_final = {p: e for p, e in escanos_asignados.items() if e > 0}
        
        # Ordenamos el diccionario final por número de escaños para que se vea bonito
        resultado_ordenado = dict(sorted(resultado_final.items(), key=lambda item: item[1], reverse=True))
        
        return resultado_ordenado, total_escanos_a_repartir
                