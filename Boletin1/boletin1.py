from datetime import*
import csv


class Asignatura:

    def __init__(self,nombre,creditos,curso,cuatrimestre):
        self.nombre = str(nombre)
        self.creditos = float(creditos)
        self.curso = int(curso) if 1 <= int(curso) <= 4 else 1
        self.cuatrimestre = int(cuatrimestre) if 1 <= int(cuatrimestre) <= 2 else 1

    def set_curso(self,curso):
        self.curso = int(curso) if 1 <= int(curso) <= 4 else 1

    def set_cuatrimestre(self,cuatrimestre):
        self.cuatrimestre = int(cuatrimestre) if 1 <= int(cuatrimestre) <= 2 else 1


class Persona:

    def __init__(self,apellidos,nombre,dni,fecha_nacimiento):
        self.apellidos = str(apellidos)
        self.nombre = str(nombre)
        self.dni = str(dni)
        self.fecha_nacimiento = date.fromisoformat(fecha_nacimiento)

    def getEdad(self):
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year

        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1

        return edad
    

class Alumno(Persona):

    def __init__(self,apellidos,nombre,dni,fecha_nacimiento,asignaturas,grupo):
        super().__init__(apellidos, nombre, dni, fecha_nacimiento)
        self.asignaturas =  asignaturas   
        self.grupo = int(grupo)

    def set_grupo(self,grupo_nuevo):

        self.grupo = int(grupo_nuevo)

    def getNumeroCreditosSuperados(self):
        return sum(asig.creditos for asig, nota in self.asignaturas if nota >= 5)
    
    def getNotaMedia(self):
        if not self.asignaturas:
            return 0.0
        total_notas = sum(nota for asig, nota in self.asignaturas)
        return total_notas / len(self.asignaturas)


class Profesor(Persona):

    def __init__(self,apellidos,nombre,dni,fecha_nacimiento,nombre_asignatura,alumnos):
        super().__init__(apellidos,nombre,dni,fecha_nacimiento)
        self.nombre_asignatura = nombre_asignatura
        self.alumnos = list(alumnos)
    
    def set_nota_alumno(self,dni,nota_actualizada):
        for alumno in self.alumnos:
            if alumno.dni == dni:
                for i,(asignatura,nota_actual) in enumerate(alumno.asignaturas):
                    if asignatura.nombre == self.nombre_asignatura:
                        alumno.asignaturas[i] = (asignatura,float(nota_actualizada))
    
    def mostrar_alumnos(self):
        for i in self.alumnos:
    # 1. Llamamos al método con paréntesis: i.getEdad()
    # 2. Calculamos media y créditos para que la info sea útil
            media = i.getNotaMedia()
            creditos = i.getNumeroCreditosSuperados()
    
    # 3. Usamos \n para el salto de línea al final
            print(f"Alumno: {i.apellidos}, {i.nombre}")
            print(f"DNI: {i.dni} | Edad: {i.getEdad()} | Grupo: {i.grupo}")
            print(f"Expediente: Media de {media:.2f} con {creditos} créditos aprobados")
            print("-" * 40 + "\n")

    

        


def cargar_datos():
    # 1. Cargar Asignaturas en un diccionario para búsqueda rápida
    asignaturas_dict = {}
    with open('Boletin1/asignaturas.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            asig = Asignatura(row['nombre'], row['creditos'], row['curso'], row['cuatrimestre'])
            asignaturas_dict[asig.nombre] = asig

    # 2. Cargar Alumnos en un diccionario {dni: objeto_alumno}
    alumnos_dict = {}
    with open('Boletin1/alumnos.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Importante: el orden de los argumentos según tu clase
            alum = Alumno(
                apellidos=row['apellidos'], 
                nombre=row['nombre'], 
                dni=row['dni'], 
                fecha_nacimiento=row['fechaNac'],
                asignaturas=[], 
                grupo=row['grupo']
            )
            alumnos_dict[alum.dni] = alum

    # 3. Cargar Notas y vincular objetos
    with open("Boletin1/notas.csv", mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dni = row['dni_alumno']
            nom_asig = row['nombre_asignatura']
            nota = float(row['nota'])

            if dni in alumnos_dict and nom_asig in asignaturas_dict:
                # Buscamos el objeto asignatura y el objeto alumno
                obj_asig = asignaturas_dict[nom_asig]
                obj_alum = alumnos_dict[dni]
                
                # Añadimos la tupla (Objeto Asignatura, Nota) al alumno
                obj_alum.asignaturas.append((obj_asig, nota))
    return alumnos_dict


diccionario_alumnos = cargar_datos()


profesor_clase = Profesor(
    apellidos="Gonzalez",
    nombre="Pepe",
    dni="12345678Z",
    fecha_nacimiento="1956-05-17",
    nombre_asignatura="Todas",
    alumnos=list(diccionario_alumnos.values()) 
)





def crear_profesores_por_asignatura(diccionario_alumnos):
    # Usaremos un diccionario para almacenar los profesores: { "NombreAsignatura": objeto_profesor }
    profesores_por_asig = {}

    # 1. Recorremos todos los alumnos para ver en qué asignaturas están matriculados
    for alumno in diccionario_alumnos.values():
        for asignatura_obj, nota in alumno.asignaturas:
            nombre_asig = asignatura_obj.nombre
            
            # 2. Si aún no existe un profesor para esta asignatura, lo creamos
            if nombre_asig not in profesores_por_asig:
                profesores_por_asig[nombre_asig] = Profesor(
                    apellidos="Pendiente", 
                    nombre="Prof. " + nombre_asig, 
                    dni="00000000X", 
                    fecha_nacimiento="1980-01-01", 
                    nombre_asignatura=nombre_asig, 
                    alumnos=[]
                )
            
            # 3. Añadimos al alumno a la lista de ese profesor si no está ya
            if alumno not in profesores_por_asig[nombre_asig].alumnos:
                profesores_por_asig[nombre_asig].alumnos.append(alumno)
                
    return profesores_por_asig

dic_profesores = crear_profesores_por_asignatura(diccionario_alumnos)

for i in dic_profesores.values():
    print(f"Profesor de {i.nombre_asignatura}"+"\n")
    i.mostrar_alumnos()
            
               








