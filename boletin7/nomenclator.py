from nombre import Nombre

class Nomenclator:
    def __init__(self):
        """
        Clase principal que centraliza la información de todos los nombres.
        
        Atributos:
            self.nombres (dict): Diccionario donde la clave es una tupla (texto, es_hombre)
                                 y el valor es la instancia del objeto Nombre.
        """
        # Estructura: {(str, bool): <objeto Nombre>}
        self.nombres = {}

    def obtener_nombre(self, texto, es_hombre):
        """
        Recupera un objeto Nombre del diccionario. Si no existe, lo crea.
        Este método será útil para que la Factoría pueda obtener la instancia 
        correcta y añadirle los datos de la década.
        """
        clave = (texto.upper(), es_hombre)
        
        if clave not in self.nombres:
            # Importante: Aquí se asume que la clase Nombre está disponible 
            # o se importará al principio del archivo.
            from nombre import Nombre
            self.nombres[clave] = Nombre(texto.upper(), es_hombre)
            
        return self.nombres[clave]

    def exportar_a_excel(self, ruta_archivo):
        """
        Exporta la información completa a un archivo Excel.
        Crea una fila por nombre y columnas para género y datos de cada década.
        """
        import openpyxl
        
        # 1. Identificar todas las décadas únicas para definir las columnas
        todas_decadas = set()
        for nombre_obj in self.nombres.values():
            for dato in nombre_obj.datos_por_decada:
                todas_decadas.add(dato.decada)
        
        # Ordenamos las décadas para que las columnas tengan sentido temporal
        decadas_lista = sorted(list(todas_decadas))

        # 2. Crear el libro y la hoja de Excel
        wb = openpyxl.Workbook()
        hoja = wb.active
        hoja.title = "Nomenclator"

        # 3. Crear y escribir la fila de cabeceras
        cabeceras = ["Nombre", "Género"]
        for decada in decadas_lista:
            cabeceras.append(f"{decada} (Frec)")
            cabeceras.append(f"{decada} (TPM)")
        hoja.append(cabeceras)

        # 4. Escribir los datos de cada nombre
        for nombre_obj in self.nombres.values():
            genero = "Hombre" if nombre_obj.es_hombre else "Mujer"
            fila = [nombre_obj.texto, genero]
            
            # Mapeamos los datos de este objeto para buscarlos por década fácilmente
            datos_map = {d.decada: d for d in nombre_obj.datos_por_decada}
            
            for decada in decadas_lista:
                if decada in datos_map:
                    fila.append(datos_map[decada].frecuencia_abs)
                    fila.append(datos_map[decada].tanto_por_mil)
                else:
                    # Si el nombre no aparece en esa década, ponemos 0
                    fila.append(0)
                    fila.append(0.0)
            
            hoja.append(fila)

        # 5. Guardar el archivo en la ruta especificada
        wb.save(ruta_archivo)


    def nombre_mas_frecuente(self, es_hombre=None):
        """
        Devuelve el objeto Nombre con mayor frecuencia absoluta acumulada.
        es_hombre: True (solo hombres), False (solo mujeres), None (ambos).
        """
        nombres_filtrados = []
        for obj_nombre in self.nombres.values():
            if es_hombre is None or obj_nombre.es_hombre == es_hombre:
                nombres_filtrados.append(obj_nombre)
        
        if not nombres_filtrados:
            return None

        # Usamos max() para encontrar el que tiene la mayor frecuencia acumulada
        nombre_max = max(nombres_filtrados, key=lambda n: n.frecuencia_acumulada)
        
        return nombre_max
    

    def n_nombres_mas_usados(self, n, es_hombre=None):
        """
        Devuelve una lista con los 'n' objetos Nombre más usados en el histórico.
        es_hombre: True (solo hombres), False (solo mujeres), None (ambos).
        """
        nombres_filtrados = []
        for obj_nombre in self.nombres.values():
            if es_hombre is None or obj_nombre.es_hombre == es_hombre:
                nombres_filtrados.append(obj_nombre)
        
        # Ordenamos la lista de mayor a menor (reverse=True) usando la frecuencia acumulada
        nombres_ordenados = sorted(nombres_filtrados, key=lambda x: x.frecuencia_acumulada, reverse=True)
        
        # Devolvemos solo los primeros 'n' elementos
        return nombres_ordenados[:n]
    

    def frecuencias_iniciales_por_decada(self, es_hombre=None):
        """
        Devuelve un diccionario {Inicial: [(Década, Frec_Acumulada), ...]} 
        con la suma de frecuencias absolutas por década para cada inicial.
        """
        # 1. Diccionario temporal para ir sumando: {Inicial: {Decada: Suma}}
        temp_sumas = {}

        # Recorremos todos los nombres filtrando por género
        for obj_nombre in self.nombres.values():
            if es_hombre is None or obj_nombre.es_hombre == es_hombre:
                inicial = obj_nombre.texto[0]
                
                # Inicializamos la letra en el diccionario si no existe
                if inicial not in temp_sumas:
                    temp_sumas[inicial] = {}
                
                # Sumamos las frecuencias de este nombre en sus décadas correspondientes
                for dato in obj_nombre.datos_por_decada:
                    decada = dato.decada
                    frecuencia = dato.frecuencia_abs
                    
                    if decada not in temp_sumas[inicial]:
                        temp_sumas[inicial][decada] = 0
                        
                    temp_sumas[inicial][decada] += frecuencia

        # 2. Transformamos el diccionario temporal al formato final: {Inicial: [(Decada, Suma)]}
        diccionario_final = {}
        for inicial, decadas_dict in temp_sumas.items():
            # Convertimos el diccionario interno en una lista de tuplas (Década, Frecuencia)
            lista_tuplas = list(decadas_dict.items())
            
            # Ordenamos la lista por el nombre de la década para que quede ordenado
            lista_tuplas.sort(key=lambda x: x[0])
            
            diccionario_final[inicial] = lista_tuplas

        return diccionario_final
    

    def inicial_mas_frecuente_por_decada(self, es_hombre=None):
        """
        Devuelve un diccionario {Década: (Letra_Mas_Frecuente, Porcentaje)} 
        basado en los datos de frecuencias por inicial.
        """
        # 1. Llamamos a la función anterior para obtener los datos
        datos_iniciales = self.frecuencias_iniciales_por_decada(es_hombre)
        
        # 2. Reestructuramos el diccionario para agrupar por década
        # Formato temporal: {Decada: {Inicial: Frecuencia}}
        datos_por_decada = {}
        for inicial, lista_decadas in datos_iniciales.items():
            for decada, frecuencia in lista_decadas:
                if decada not in datos_por_decada:
                    datos_por_decada[decada] = {}
                datos_por_decada[decada][inicial] = frecuencia
                
        # 3. Calculamos la letra ganadora y su porcentaje para cada década
        resultado_final = {}
        for decada, letras_dict in datos_por_decada.items():
            # Sumamos todos los nacimientos de esa década (de todas las iniciales)
            total_decada = sum(letras_dict.values())
            
            # Buscamos la inicial que tiene el valor (frecuencia) máximo
            # .items() devuelve tuplas (letra, frec), ordenamos por el elemento [1]
            tupla_max = max(letras_dict.items(), key=lambda x: x[1])
            letra_ganadora = tupla_max[0]
            frecuencia_maxima = tupla_max[1]
            
            # Calculamos el porcentaje y lo redondeamos a 2 decimales
            porcentaje = (frecuencia_maxima / total_decada) * 100
            
            resultado_final[decada] = (letra_ganadora, round(porcentaje, 2))
            
        # 4. Ordenamos el diccionario resultante cronológicamente por la clave (década)
        resultado_ordenado = dict(sorted(resultado_final.items()))
        
        return resultado_ordenado
    

    def evolucion_nombres_compuestos(self, es_hombre=None):
        """
        Calcula el porcentaje de nombres simples vs compuestos por década.
        Devuelve una lista de tuplas: [(Década, %Simples, %Compuestos), ...]
        """
        # 1. Diccionario de contadores: {Década: [Frec_Simples, Frec_Compuestos]}
        # Usamos una lista de 2 elementos para poder ir sumando fácilmente
        conteo_decadas = {}

        for obj_nombre in self.nombres.values():
            if es_hombre is None or obj_nombre.es_hombre == es_hombre:
                # Un nombre es compuesto si contiene un espacio en blanco
                es_compuesto = " " in obj_nombre.texto.strip()
                
                for dato in obj_nombre.datos_por_decada:
                    decada = dato.decada
                    if decada not in conteo_decadas:
                        conteo_decadas[decada] = [0, 0] # [Simples, Compuestos]
                    
                    if es_compuesto:
                        conteo_decadas[decada][1] += dato.frecuencia_abs
                    else:
                        conteo_decadas[decada][0] += dato.frecuencia_abs

        # 2. Convertir a porcentajes y ordenar temporalmente
        resultado_final = []
        decadas_ordenadas = sorted(conteo_decadas.keys())

        for decada in decadas_ordenadas:
            simples, compuestos = conteo_decadas[decada]
            total = simples + compuestos
            
            if total > 0:
                perc_simple = (simples / total) * 100
                perc_compuesto = (compuestos / total) * 100
                resultado_final.append((
                    decada, 
                    round(perc_simple, 2), 
                    round(perc_compuesto, 2)
                ))

        return resultado_final
    


    def longitud_media_por_decada(self, es_hombre=None):
        """
        Calcula la longitud media de los nombres ponderada por su frecuencia.
        Devuelve una lista de tuplas: [(Década, Longitud_Media), ...] ordenada.
        """
        # Diccionario para acumular: {Década: [Suma_Longitudes, Total_Frecuencias]}
        datos_decada = {}

        for obj_nombre in self.nombres.values():
            if es_hombre is None or obj_nombre.es_hombre == es_hombre:
                # Calculamos las letras del nombre (quitando posibles espacios extra)
                longitud_nombre = len(obj_nombre.texto.strip())
                
                for dato in obj_nombre.datos_por_decada:
                    decada = dato.decada
                    
                    if decada not in datos_decada:
                        datos_decada[decada] = [0, 0]
                    
                    # Ponderamos: multiplicamos la longitud del nombre por las veces que se puso
                    datos_decada[decada][0] += longitud_nombre * dato.frecuencia_abs
                    # Sumamos el total de personas
                    datos_decada[decada][1] += dato.frecuencia_abs

        # Calculamos la media final y la guardamos en una lista
        resultado_final = []
        decadas_ordenadas = sorted(datos_decada.keys())

        for decada in decadas_ordenadas:
            suma_longitudes, total_personas = datos_decada[decada]
            
            if total_personas > 0:
                # Media = Suma de todas las letras / Total de personas
                media = suma_longitudes / total_personas
                resultado_final.append((decada, round(media, 2)))

        return resultado_final
    


    def nombres_en_n_decadas(self, n, es_hombre=None):
        """
        Devuelve una lista de objetos Nombre que han estado entre los 
        más frecuentes durante al menos 'n' décadas.
        """
        nombres_persistentes = []

        for obj_nombre in self.nombres.values():
            # Filtramos por género
            if es_hombre is None or obj_nombre.es_hombre == es_hombre:
                
                # Comprobamos si el número de décadas registradas es mayor o igual a 'n'
                if len(obj_nombre.datos_por_decada) >= n:
                    nombres_persistentes.append(obj_nombre)

        # Ordenamos la lista para que salgan primero los que han estado en MÁS décadas
        # y en caso de empate, los que tengan mayor frecuencia acumulada
        nombres_persistentes.sort(
            key=lambda x: (len(x.datos_por_decada), x.frecuencia_acumulada), 
            reverse=True
        )

        return nombres_persistentes
    


    def modas_pasajeras_al_principio(self, n, es_hombre=None):
        """
        Devuelve una lista de nombres que solo estuvieron en el Top 50 durante 
        las 'n' primeras décadas (o menos) y luego no volvieron a aparecer.
        """
        import re

        # 1. Obtener todas las décadas únicas de nuestro Nomenclator
        decadas_set = set()
        for obj in self.nombres.values():
            for dato in obj.datos_por_decada:
                decadas_set.add(dato.decada)
                
        # Función auxiliar para enseñar a Python a ordenar las décadas cronológicamente
        def clave_orden(d):
            # A "ANTES DE 1930" le damos el valor 0 para que vaya la primera
            if "ANTES" in d.upper():
                return 0
            # Para el resto, buscamos el primer número de 4 cifras (ej: "1930")
            match = re.search(r'\d{4}', d)
            return int(match.group(0)) if match else 9999
            
        # Ordenamos las décadas de más antigua a más reciente
        decadas_ordenadas = sorted(list(decadas_set), key=clave_orden)
        
        # 2. Recortar la lista para quedarnos solo con las 'n' primeras décadas
        decadas_permitidas = set(decadas_ordenadas[:n])
        
        nombres_olvidados = []
        
        # 3. Buscar qué nombres cumplen la condición
        for obj_nombre in self.nombres.values():
            if es_hombre is None or obj_nombre.es_hombre == es_hombre:
                
                # Sacamos un conjunto (set) con las décadas en las que aparece este nombre
                decadas_del_nombre = {dato.decada for dato in obj_nombre.datos_por_decada}
                
                # Condición: Que tenga al menos una década, y que TODAS sus décadas 
                # estén dentro del conjunto de décadas_permitidas
                if decadas_del_nombre and decadas_del_nombre.issubset(decadas_permitidas):
                    nombres_olvidados.append(obj_nombre)
                    
        # 4. Ordenamos el resultado para ver primero los más frecuentes dentro de su época
        nombres_olvidados.sort(key=lambda x: x.frecuencia_acumulada, reverse=True)
        
        return nombres_olvidados
    


    def modas_recientes(self, n, es_hombre=None):
        """
        Devuelve una lista de nombres que solo han aparecido en el Top 50 
        durante las últimas 'n' décadas (o menos).
        """
        import re

        # 1. Obtener y ordenar las décadas cronológicamente
        decadas_set = set()
        for obj in self.nombres.values():
            for dato in obj.datos_por_decada:
                decadas_set.add(dato.decada)
                
        def clave_orden(d):
            if "ANTES" in d.upper():
                return 0
            match = re.search(r'\d{4}', d)
            return int(match.group(0)) if match else 9999
            
        decadas_ordenadas = sorted(list(decadas_set), key=clave_orden)
        
        # 2. Recortar la lista para quedarnos solo con las ÚLTIMAS 'n' décadas
        # Usamos [-n:] para coger desde el final hacia atrás
        ultimas_decadas = set(decadas_ordenadas[-n:])
        
        nombres_recientes = []
        
        # 3. Buscar qué nombres cumplen la condición
        for obj_nombre in self.nombres.values():
            if es_hombre is None or obj_nombre.es_hombre == es_hombre:
                
                decadas_del_nombre = {dato.decada for dato in obj_nombre.datos_por_decada}
                
                # Condición: Que tenga al menos una década, y que TODAS sus décadas 
                # pertenezcan exclusivamente al grupo de las últimas décadas.
                if decadas_del_nombre and decadas_del_nombre.issubset(ultimas_decadas):
                    nombres_recientes.append(obj_nombre)
                    
        # 4. Ordenamos para ver primero los más frecuentes
        nombres_recientes.sort(key=lambda x: x.frecuencia_acumulada, reverse=True)
        
        return nombres_recientes
    



    def nombres_resurgidos(self, n, m, es_hombre=None):
        """
        Devuelve los nombres que estuvieron 'n' décadas presentes, 
        luego 'm' décadas ausentes, y volvieron a reaparecer.
        """
        import re

        # 1. Obtener y ordenar todas las décadas cronológicamente
        decadas_set = set()
        for obj in self.nombres.values():
            for dato in obj.datos_por_decada:
                decadas_set.add(dato.decada)
                
        def clave_orden(d):
            if "ANTES" in d.upper():
                return 0
            match = re.search(r'\d{4}', d)
            return int(match.group(0)) if match else 9999
            
        decadas_ordenadas = sorted(list(decadas_set), key=clave_orden)
        
        nombres_encontrados = []
        
        # 2. Construimos el "patrón" que queremos buscar.
        # Ej: si n=2 y m=3, el patrón será "110001" (2 presencias, 3 ausencias, 1 presencia)
        patron_buscado = ("1" * n) + ("0" * m) + "1"
        
        # 3. Analizamos la "línea temporal" de cada nombre
        for obj_nombre in self.nombres.values():
            if es_hombre is None or obj_nombre.es_hombre == es_hombre:
                
                decadas_del_nombre = {dato.decada for dato in obj_nombre.datos_por_decada}
                
                # Creamos el mapa temporal del nombre (ej: "111001011")
                mapa_temporal = ""
                for decada in decadas_ordenadas:
                    if decada in decadas_del_nombre:
                        mapa_temporal += "1"
                    else:
                        mapa_temporal += "0"
                        
                # Si nuestro patrón está dentro del mapa temporal, ¡hizo un resurgimiento!
                if patron_buscado in mapa_temporal:
                    nombres_encontrados.append(obj_nombre)
                    
        # 4. Ordenamos para ver primero los más frecuentes
        nombres_encontrados.sort(key=lambda x: x.frecuencia_acumulada, reverse=True)
        
        return nombres_encontrados
    


    def guardar_grafica_tendencia_tpm(self, lista_nombres, nombre_archivo="tendencia_nombres.png",es_hombre=None):
        """
        Dada una lista de strings con nombres, dibuja una gráfica de líneas
        con la evolución de su Tasa Por Mil (TPM) a lo largo de las décadas.
        Requiere tener instalada la librería matplotlib.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Error: Necesitas instalar matplotlib para ver la gráfica (ejecuta: pip install matplotlib)")
            return
            
        import re

        # 1. Obtener y ordenar todas las décadas cronológicamente
        decadas_set = set()
        for obj in self.nombres.values():
            for dato in obj.datos_por_decada:
                decadas_set.add(dato.decada)
                
        def clave_orden(d):
            if "ANTES" in d.upper():
                return 0
            match = re.search(r'\d{4}', d)
            return int(match.group(0)) if match else 9999
            
        decadas_ordenadas = sorted(list(decadas_set), key=clave_orden)
        
        # 2. Preparar el lienzo de la gráfica
        plt.figure(figsize=(12, 6))
        
        # 3. Buscar y extraer los datos para cada nombre de la lista
        for nombre_buscado in lista_nombres:
            nombre_buscado = nombre_buscado.strip().upper()
            
            # Buscamos el objeto Nombre que coincida con el texto
            obj_encontrado = None
            for obj in self.nombres.values():
                if obj.texto == nombre_buscado:
                    if es_hombre is None or obj.es_hombre == es_hombre:
                        obj_encontrado = obj
                        break 
                        
            if obj_encontrado:
                # Diccionario temporal para buscar rápido el TPM por década
                dicc_tpm = {dato.decada: dato.tanto_por_mil for dato in obj_encontrado.datos_por_decada}
                
                # Creamos la lista de valores Y (si no existe en esa década, es 0)
                valores_y = [dicc_tpm.get(dec, 0) for dec in decadas_ordenadas]
                
                # Añadimos la línea de este nombre a la gráfica
                plt.plot(decadas_ordenadas, valores_y, marker='o', label=nombre_buscado)
            else:
                print(f"Aviso: No se encontró el nombre '{nombre_buscado}'.")

        # 4. Configurar detalles estéticos
        plt.title("Evolución de la popularidad de los nombres")
        plt.xlabel("Décadas")
        plt.ylabel("Tantos por mil (‰)")
        plt.xticks(rotation=45) # Inclinamos el texto de las décadas para que quepa bien
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout() 
        
        # 5. GUARDAR EN VEZ DE MOSTRAR
        plt.savefig(nombre_archivo)
        plt.close() # Cerramos la figura para liberar memoria
        print(f"ÉXITO: Gráfica guardada correctamente en '{nombre_archivo}'")


    def mayor_incremento_tpm(self, n, es_hombre=None):
        """
        Devuelve los 'n' nombres con el mayor incremento absoluto de 
        Tanto por Mil (TPM) entre dos décadas consecutivas.
        """
        import re

        # 1. Obtener y ordenar todas las décadas cronológicamente
        decadas_set = set()
        for obj in self.nombres.values():
            for dato in obj.datos_por_decada:
                decadas_set.add(dato.decada)
                
        def clave_orden(d):
            if "ANTES" in d.upper():
                return 0
            match = re.search(r'\d{4}', d)
            return int(match.group(0)) if match else 9999
            
        decadas_ordenadas = sorted(list(decadas_set), key=clave_orden)
        
        resultados = []
        
        # 2. Calcular el mayor salto para cada nombre
        for obj_nombre in self.nombres.values():
            if es_hombre is None or obj_nombre.es_hombre == es_hombre:
                
                # Diccionario para acceder rápidamente al TPM de cada década. 
                # Si no está, asumiremos que es 0.
                dicc_tpm = {dato.decada: dato.tanto_por_mil for dato in obj_nombre.datos_por_decada}
                
                max_incremento = 0
                dec_origen = ""
                dec_destino = ""
                
                # Iteramos comparando cada década con la inmediatamente siguiente
                for i in range(len(decadas_ordenadas) - 1):
                    dec_actual = decadas_ordenadas[i]
                    dec_siguiente = decadas_ordenadas[i + 1]
                    
                    tpm_actual = dicc_tpm.get(dec_actual, 0)
                    tpm_siguiente = dicc_tpm.get(dec_siguiente, 0)
                    
                    # Calculamos cuánto subió
                    incremento = tpm_siguiente - tpm_actual
                    
                    # Si este salto es el más grande que ha dado este nombre, lo guardamos
                    if incremento > max_incremento:
                        max_incremento = incremento
                        dec_origen = dec_actual
                        dec_destino = dec_siguiente
                        
                # Si el nombre tuvo al menos un incremento positivo en su historia, lo añadimos
                if max_incremento > 0:
                    resultados.append({
                        'objeto': obj_nombre,
                        'incremento': max_incremento,
                        'desde': dec_origen,
                        'hasta': dec_destino
                    })
                    
        # 3. Ordenar todos los resultados por el tamaño del salto (de mayor a menor)
        resultados.sort(key=lambda x: x['incremento'], reverse=True)
        
        # 4. Devolver solo los 'n' primeros
        return resultados[:n]
    

    def concentracion_top_n(self, n, es_hombre=None):
        """
        Calcula la concentración de los 'n' nombres más frecuentes por década.
        Devuelve un diccionario {decada: suma_tpm_top_n} ordenado cronológicamente.
        """
        import re
        
        # 1. Agrupamos todos los TPM por década
        # Quedará algo así: {'1930 A 1939': [15.2, 10.5, 8.1, ...], ...}
        tpms_por_decada = {}

        for obj_nombre in self.nombres.values():
            if es_hombre is None or obj_nombre.es_hombre == es_hombre:
                for dato in obj_nombre.datos_por_decada:
                    if dato.decada not in tpms_por_decada:
                        tpms_por_decada[dato.decada] = []
                    # Guardamos el TPM de este nombre en su década correspondiente
                    tpms_por_decada[dato.decada].append(dato.tanto_por_mil)

        # 2. Función auxiliar para ordenar las décadas cronológicamente
        def clave_orden(d):
            if "ANTES" in d.upper():
                return 0
            match = re.search(r'\d{4}', d)
            return int(match.group(0)) if match else 9999

        # 3. Calculamos la suma de los 'n' mayores para cada década
        resultado = {}
        decadas_ordenadas = sorted(tpms_por_decada.keys(), key=clave_orden)

        for decada in decadas_ordenadas:
            lista_tpms = tpms_por_decada[decada]
            
            # Ordenamos la lista de TPMs de esta década de mayor a menor
            lista_tpms.sort(reverse=True)
            
            # Cogemos los 'n' primeros y los sumamos
            suma_top_n = sum(lista_tpms[:n])
            
            # Guardamos redondeando a 2 decimales para que sea legible
            resultado[decada] = round(suma_top_n, 2)

        return resultado
    

    def guardar_grafica_concentracion(self, n, nombre_archivo="concentracion_nombres.png", es_hombre=None):
        """
        Genera una gráfica de líneas mostrando la evolución de la concentración 
        de los 'n' nombres más comunes y la guarda como archivo PNG.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Error: Necesitas instalar matplotlib (ejecuta: pip install matplotlib)")
            return

        plt.figure(figsize=(10, 6))
        
        # Obtenemos y dibujamos los datos de mujeres si corresponde
        if es_hombre is None or es_hombre is False:
            datos_mujeres = self.concentracion_top_n(n, es_hombre=False)
            decadas = list(datos_mujeres.keys())
            valores = list(datos_mujeres.values())
            # Usamos un color distintivo y marcadores circulares
            plt.plot(decadas, valores, marker='o', color='purple', label='Mujeres', linewidth=2)

        # Obtenemos y dibujamos los datos de hombres si corresponde
        if es_hombre is None or es_hombre is True:
            datos_hombres = self.concentracion_top_n(n, es_hombre=True)
            decadas = list(datos_hombres.keys())
            valores = list(datos_hombres.values())
            plt.plot(decadas, valores, marker='s', color='green', label='Hombres', linewidth=2)

        # Configuramos los aspectos visuales del gráfico
        plt.title(f"Evolución de la concentración: Top {n} nombres más comunes")
        plt.xlabel("Décadas")
        plt.ylabel("Suma del Tanto por mil (‰)")
        plt.xticks(rotation=45) # Inclinamos las etiquetas del eje X
        
        # Añadimos la leyenda, una cuadrícula y ajustamos los márgenes
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Guardamos en disco y cerramos la figura (sin mostrar ventana emergente)
        plt.savefig(nombre_archivo)
        plt.close()
        
        print(f"ÉXITO: Gráfica de diversificación guardada en '{nombre_archivo}'")