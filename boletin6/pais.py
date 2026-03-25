import matplotlib.pyplot as plt
import itertools

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
    

    def comprobar_escanos_excel(self):
        """
        Audita todas las provincias comparando los escaños reales del Excel
        con los calculados por nuestro algoritmo D'Hondt.
        """
        provincias_totales = 0
        provincias_correctas = 0
        discrepancias = [] # Aquí guardaremos los chivatazos de error

        for comunidad in self.comunidades_autonomas.values():
            for provincia in comunidad.provincias.values():
                provincias_totales += 1
                
                # 1. Obtener los escaños reales directamente del Excel
                escanos_reales = {}
                for partido, (votos, diputados) in provincia.resultados_partidos.items():
                    if diputados > 0:
                        escanos_reales[partido] = diputados
                
                # 2. Obtener los escaños calculados por nuestro propio algoritmo
                escanos_calculados, escanos_totales = self.calcular_escanos_dhondt(comunidad.nombre, provincia.nombre)
                
                # Si la provincia no repartía escaños (o hubo un error de lectura), la saltamos
                if escanos_totales == 0:
                    continue

                # 3. Comparar frente a frente
                if escanos_reales == escanos_calculados:
                    provincias_correctas += 1
                else:
                    # Si no coinciden, guardamos el informe del error
                    discrepancias.append({
                        'comunidad': comunidad.nombre,
                        'provincia': provincia.nombre,
                        'reales': escanos_reales,
                        'calculados': escanos_calculados
                    })

        # Devolvemos el resumen de la auditoría
        return provincias_totales, provincias_correctas, discrepancias
    
    def simular_congreso_nacional(self):
        """
        Calcula la composición total del Congreso de los Diputados (350 escaños)
        sumando los resultados D'Hondt de las 52 provincias.
        """
        congreso = {}
        
        # Recorremos todas las comunidades y provincias
        for comunidad in self.comunidades_autonomas.values():
            for provincia in comunidad.provincias.values():
                
                # Usamos el método D'Hondt que ya sabemos que funciona al 100%
                escanos_provincia, total = self.calcular_escanos_dhondt(comunidad.nombre, provincia.nombre)
                
                # Sumamos los escaños obtenidos al total nacional del partido
                for partido, escanos in escanos_provincia.items():
                    if partido in congreso:
                        congreso[partido] += escanos
                    else:
                        congreso[partido] = escanos
                        
        # Ordenamos el resultado final de mayor a menor número de escaños
        congreso_ordenado = dict(sorted(congreso.items(), key=lambda item: item[1], reverse=True))
        
        return congreso_ordenado
    


    def graficar_escanos(self, nivel="nacional", id_comunidad=None, id_provincia=None):
        """
        Genera un gráfico de barras con el reparto de escaños a nivel nacional,
        autonómico o provincial.
        """
        datos_grafica = {}
        titulo = ""

        # 1. RECOPILACIÓN DE DATOS SEGÚN EL NIVEL
        if nivel == "nacional":
            # Llamamos a nuestro simulador del Congreso
            datos_grafica = self.simular_congreso_nacional()
            total_escanos = sum(datos_grafica.values())
            titulo = f"Reparto de Escaños - NACIONAL (Total: {total_escanos} diputados)"

        elif nivel == "comunidad":
            if not id_comunidad:
                print("Error: Debes indicar el id_comunidad para el nivel autonómico.")
                return

            # Buscamos la comunidad de forma robusta
            comunidad_obj = None
            for com in self.comunidades_autonomas.values():
                if str(id_comunidad).lower() in com.nombre.lower():
                    comunidad_obj = com
                    break
            
            if not comunidad_obj:
                print(f"Error: Comunidad '{id_comunidad}' no encontrada.")
                return

            # Sumamos los escaños D'Hondt de todas sus provincias
            for prov in comunidad_obj.provincias.values():
                escanos_prov, _ = self.calcular_escanos_dhondt(comunidad_obj.nombre, prov.nombre)
                for partido, escanos in escanos_prov.items():
                    if partido in datos_grafica:
                        datos_grafica[partido] += escanos
                    else:
                        datos_grafica[partido] = escanos
            
            # Ordenamos el diccionario resultante de mayor a menor
            datos_grafica = dict(sorted(datos_grafica.items(), key=lambda x: x[1], reverse=True))
            total_escanos = sum(datos_grafica.values())
            titulo = f"Reparto de Escaños - {comunidad_obj.nombre.upper()} (Total: {total_escanos})"

        elif nivel == "provincial":
            if not id_comunidad or not id_provincia:
                print("Error: Faltan datos de comunidad o provincia.")
                return
            
            # Llamamos directamente a D'Hondt
            datos_grafica, total_escanos = self.calcular_escanos_dhondt(id_comunidad, id_provincia)
            if not datos_grafica:
                return # Si hubo error, el método D'Hondt ya imprimió el mensaje
                
            titulo = f"Reparto D'Hondt - Provincia: {str(id_provincia).upper()} (Total: {total_escanos})"
            
        else:
            print("Nivel no reconocido. Usa 'nacional', 'comunidad' o 'provincial'.")
            return

        # 2. CREACIÓN DE LA GRÁFICA CON MATPLOTLIB
        if not datos_grafica:
            print("No hay datos de escaños para graficar.")
            return

        # Extraemos las listas de partidos y sus escaños
        partidos = list(datos_grafica.keys())
        escanos = list(datos_grafica.values())

        # Configuramos el tamaño de la ventana
        plt.figure(figsize=(12, 7))
        
        # Creamos el gráfico de barras
        barras = plt.bar(partidos, escanos, color='#4A90E2', edgecolor='black')
        
        # Añadimos el número exacto encima de cada barra para que sea más legible
        for barra in barras:
            altura = barra.get_height()
            plt.text(barra.get_x() + barra.get_width()/2, altura + 0.3, 
                     int(altura), ha='center', va='bottom', fontweight='bold')

        # Títulos y etiquetas
        plt.title(titulo, fontsize=14, fontweight='bold', pad=20)
        plt.ylabel("Número de Escaños", fontsize=12)
        
        # Rotamos los nombres de los partidos 45 grados para que no se superpongan
        plt.xticks(rotation=45, ha='right', fontsize=9)
        
        # Ajustamos los márgenes automáticamente para que no se corte el texto de abajo
        plt.tight_layout()
        
        # Mostramos la gráfica en pantalla
        plt.show()



    def analizar_ultimo_escano(self):
        """
        Analiza en cada provincia qué partido se llevó el último escaño,
        qué partido se quedó más cerca de arrebatárselo, y por cuántos votos.
        """
        resultados = []

        for comunidad in self.comunidades_autonomas.values():
            for provincia in comunidad.provincias.values():
                
                # 1. Extraemos votos y calculamos el total de escaños reales de la provincia
                votos_partidos = {p: v for p, (v, d) in provincia.resultados_partidos.items() if v > 0}
                total_escanos = sum(d for v, d in provincia.resultados_partidos.values())
                
                if total_escanos == 0 or len(votos_partidos) < 2:
                    continue

                # 2. Generamos la tabla completa de cocientes D'Hondt
                cocientes = []
                for partido, votos in votos_partidos.items():
                    # Usamos total_escanos + 2 para garantizar que calculamos suficientes 
                    # cocientes "perdedores" en el ranking.
                    for divisor in range(1, total_escanos + 2): 
                        cociente = votos / divisor
                        cocientes.append((cociente, votos, partido, divisor))

                # 3. Ordenamos de mayor a menor (desempate por votos totales)
                cocientes.sort(key=lambda x: (x[0], x[1]), reverse=True)

                # 4. El último escaño es el que ocupa la posición 'total_escanos - 1'
                ultimo_ganador = cocientes[total_escanos - 1]
                cociente_ganador = ultimo_ganador[0]
                partido_ganador = ultimo_ganador[2]

                # 5. Buscamos al primer perdedor que NO sea el propio partido ganador
                # (queremos saber quién le habría quitado el escaño desde fuera)
                perdedores = cocientes[total_escanos:]
                partido_perdedor = None
                
                for perdedor in perdedores:
                    if perdedor[2] != partido_ganador:
                        votos_totales_perdedor = perdedor[1]
                        partido_perdedor = perdedor[2]
                        divisor_perdedor = perdedor[3]
                        break
                
                # 6. Cálculo matemático de los votos faltantes
                if partido_perdedor:
                    # Para ganar, el perdedor necesitaba que: Votos_Nuevos / Divisor > Cociente_Ganador
                    # Despejamos: Votos_Nuevos = (Cociente_Ganador * Divisor) + 1
                    votos_necesarios = int(cociente_ganador * divisor_perdedor) + 1
                    votos_faltantes = votos_necesarios - votos_totales_perdedor
                    
                    resultados.append({
                        'comunidad': comunidad.nombre,
                        'provincia': provincia.nombre,
                        'ganador': partido_ganador,
                        'perdedor': partido_perdedor,
                        'votos_faltantes': votos_faltantes
                    })

        # 7. Ordenamos todo el país de menor a mayor diferencia de votos
        resultados.sort(key=lambda x: x['votos_faltantes'])
        
        return resultados
    

    def coste_del_escano(self):
        """
        Calcula la ratio de votos necesarios por cada escaño conseguido.
        Devuelve dos rankings ordenados de más barato a más caro:
        uno a nivel nacional y otro a nivel provincial.
        """
        # 1. Variables para acumular datos
        votos_nacionales = {}
        escanos_nacionales = {}
        ranking_provincial = []

        # 2. Recorremos todas las provincias para extraer los datos reales
        for comunidad in self.comunidades_autonomas.values():
            for provincia in comunidad.provincias.values():
                for partido, (votos, diputados) in provincia.resultados_partidos.items():
                    
                    # A. Acumulamos para el cálculo Nacional
                    votos_nacionales[partido] = votos_nacionales.get(partido, 0) + votos
                    escanos_nacionales[partido] = escanos_nacionales.get(partido, 0) + diputados
                    
                    # B. Calculamos el coste Provincial (solo si consiguieron representación)
                    if diputados > 0:
                        coste = votos / diputados
                        ranking_provincial.append({
                            'comunidad': comunidad.nombre,
                            'provincia': provincia.nombre,
                            'partido': partido,
                            'escanos': diputados,
                            'coste': coste
                        })

        # 3. Calculamos el coste Nacional (solo partidos con representación en el Congreso)
        ranking_nacional = []
        for partido, escanos in escanos_nacionales.items():
            if escanos > 0:
                votos_totales = votos_nacionales[partido]
                coste = votos_totales / escanos
                ranking_nacional.append({
                    'partido': partido,
                    'escanos': escanos,
                    'votos_totales': votos_totales,
                    'coste': coste
                })

        # 4. Ordenamos ambos rankings de más barato (menor coste) a más caro
        ranking_nacional.sort(key=lambda x: x['coste'])
        ranking_provincial.sort(key=lambda x: x['coste'])

        return ranking_nacional, ranking_provincial
    


    def escanos_mas_caros(self):
        """
        Calcula la ratio de votos necesarios por cada escaño conseguido.
        Devuelve dos rankings ordenados de MÁS CARO a más barato:
        uno a nivel nacional y otro a nivel provincial.
        """
        # 1. Variables para acumular datos
        votos_nacionales = {}
        escanos_nacionales = {}
        ranking_provincial = []

        # 2. Recorremos todas las provincias
        for comunidad in self.comunidades_autonomas.values():
            for provincia in comunidad.provincias.values():
                for partido, (votos, diputados) in provincia.resultados_partidos.items():
                    
                    # A. Acumulamos para el cálculo Nacional
                    votos_nacionales[partido] = votos_nacionales.get(partido, 0) + votos
                    escanos_nacionales[partido] = escanos_nacionales.get(partido, 0) + diputados
                    
                    # B. Calculamos el coste Provincial (solo si lograron el escaño)
                    if diputados > 0:
                        coste = votos / diputados
                        ranking_provincial.append({
                            'comunidad': comunidad.nombre,
                            'provincia': provincia.nombre,
                            'partido': partido,
                            'escanos': diputados,
                            'coste': coste
                        })

        # 3. Calculamos el coste Nacional (solo partidos con representación)
        ranking_nacional = []
        for partido, escanos in escanos_nacionales.items():
            if escanos > 0:
                votos_totales = votos_nacionales[partido]
                coste = votos_totales / escanos
                ranking_nacional.append({
                    'partido': partido,
                    'escanos': escanos,
                    'votos_totales': votos_totales,
                    'coste': coste
                })

        # 4. LA MAGIA: Ordenamos de mayor coste a menor coste (reverse=True)
        ranking_nacional.sort(key=lambda x: x['coste'], reverse=True)
        ranking_provincial.sort(key=lambda x: x['coste'], reverse=True)

        return ranking_nacional, ranking_provincial
    


    def ranking_provincias_baratas(self):
        """
        Calcula el coste medio de un escaño en cada provincia 
        (Total de votos emitidos / Total de escaños a repartir en la provincia).
        Devuelve el ranking ordenado de las provincias más "baratas" a las más "caras".
        """
        ranking_provincias = []

        # Recorremos el país provincia a provincia
        for comunidad in self.comunidades_autonomas.values():
            for provincia in comunidad.provincias.values():
                
                votos_totales_provincia = 0
                escanos_totales_provincia = 0
                
                # Sumamos todos los votos y escaños de la provincia
                for partido, (votos, diputados) in provincia.resultados_partidos.items():
                    votos_totales_provincia += votos
                    escanos_totales_provincia += diputados
                
                # Si la provincia reparte escaños, calculamos la media
                if escanos_totales_provincia > 0:
                    coste_medio = votos_totales_provincia / escanos_totales_provincia
                    
                    ranking_provincias.append({
                        'comunidad': comunidad.nombre,
                        'provincia': provincia.nombre,
                        'votos_totales': votos_totales_provincia,
                        'escanos_totales': escanos_totales_provincia,
                        'coste_medio': coste_medio
                    })

        # Ordenamos de menor a mayor coste (las más "baratas" primero)
        ranking_provincias.sort(key=lambda x: x['coste_medio'])
        
        return ranking_provincias
    


    def partido_mas_votado_sin_escano(self):
        """
        Calcula qué partido obtuvo más votos a nivel nacional en total, 
        pero no consiguió ni un solo escaño en el Congreso.
        Devuelve una lista ordenada de mayor a menor número de votos.
        """
        votos_nacionales = {}
        escanos_nacionales = {}

        # 1. Recopilar votos y escaños totales de todas las provincias
        for comunidad in self.comunidades_autonomas.values():
            for provincia in comunidad.provincias.values():
                for partido, (votos, diputados) in provincia.resultados_partidos.items():
                    votos_nacionales[partido] = votos_nacionales.get(partido, 0) + votos
                    escanos_nacionales[partido] = escanos_nacionales.get(partido, 0) + diputados

        # 2. Filtrar a los que tienen exactamente 0 escaños en TODO el país
        partidos_sin_escano = []
        for partido, escanos in escanos_nacionales.items():
            if escanos == 0:
                votos_totales = votos_nacionales[partido]
                # Los incluimos solo si sacaron al menos 1 voto real
                if votos_totales > 0:
                    partidos_sin_escano.append({
                        'partido': partido,
                        'votos': votos_totales
                    })

        # 3. Ordenar la lista de mayor cantidad de votos a menor
        partidos_sin_escano.sort(key=lambda x: x['votos'], reverse=True)

        return partidos_sin_escano
    

    def parejas_con_menos_votos(self, n=5):
        """
        Encuentra las 'n' parejas (partido - provincia) que obtuvieron
        la menor cantidad de votos, excluyendo los que sacaron 0.
        """
        resultados_validos = []

        # Recorremos todo el país
        for comunidad in self.comunidades_autonomas.values():
            for provincia in comunidad.provincias.values():
                for partido, (votos, diputados) in provincia.resultados_partidos.items():
                    
                    # Filtramos: nos interesan solo los que tienen al menos 1 voto
                    if votos > 0:
                        resultados_validos.append({
                            'comunidad': comunidad.nombre,
                            'provincia': provincia.nombre,
                            'partido': partido,
                            'votos': votos
                        })

        # Ordenamos la lista de menor a mayor cantidad de votos
        resultados_validos.sort(key=lambda x: x['votos'])

        # Devolvemos exactamente la cantidad 'n' que nos haya pedido el usuario
        return resultados_validos[:n]
    

    def pactometro(self, n=176, vetos=None):
        """
        Calcula todas las combinaciones posibles de partidos que superan 'n' escaños,
        excluyendo aquellas alianzas que contengan vetos políticos irreconciliables.
        """
        # Si no le pasamos vetos, creamos una lista vacía por defecto
        if vetos is None:
            vetos = []

        congreso = self.simular_congreso_nacional()
        partidos_con_escanos = {p: e for p, e in congreso.items() if e > 0}
        nombres_partidos = list(partidos_con_escanos.keys())
        
        combinaciones_validas = []

        for r in range(1, len(nombres_partidos) + 1):
            for combo in itertools.combinations(nombres_partidos, r):
                
                # 1. COMPROBAR VETOS (La línea roja política)
                combo_set = set(combo)
                pacto_imposible = False
                
                for linea_roja in vetos:
                    # Si todos los partidos del veto están dentro de este pacto...
                    if set(linea_roja).issubset(combo_set):
                        pacto_imposible = True
                        break # Rompemos el bucle, este pacto no nos vale
                
                # Si el pacto es imposible, saltamos a la siguiente combinación
                if pacto_imposible:
                    continue
                
                # 2. COMPROBAR MAYORÍA (La matemática)
                suma_escanos = sum(partidos_con_escanos[p] for p in combo)
                
                if suma_escanos >= n:
                    combinaciones_validas.append({
                        'partidos': combo,
                        'escanos_totales': suma_escanos
                    })
                    
        # Ordenamos por menor número de partidos implicados
        combinaciones_validas.sort(key=lambda x: (len(x['partidos']), x['escanos_totales']))
        
        return combinaciones_validas
                