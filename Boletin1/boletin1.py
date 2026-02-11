from datetime import*
import csv
from collections import defaultdict


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
    

        


def cargar_datos():
    # 1. Cargar Asignaturas en un diccionario para búsqueda rápida
    asignaturas_dict = {}
    with open('asignaturas.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            asig = Asignatura(row['nombre'], row['creditos'], row['curso'], row['cuatrimestre'])
            asignaturas_dict[asig.nombre] = asig

    # 2. Cargar Alumnos en un diccionario {dni: objeto_alumno}
    alumnos_dict = {}
    with open('alumnos.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Importante: el orden de los argumentos según tu clase
            alum = Alumno(
                apellidos=row['apellidos'], 
                nombre=row['nombre'], 
                dni=row['dni'], 
                fecha_nacimiento=row['fecha_nacimiento'], # Asegúrate de que el CSV tenga este campo
                asignaturas=[], 
                grupo=row['grupo']
            )
            alumnos_dict[alum.dni] = alum

    # 3. Cargar Notas y vincular objetos
    with open("notas.csv", mode="r", encoding="utf-8") as f:
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


# --- Mostrar resultados por pantalla ---

print(f"\n{'LISTADO DE ALUMNOS - PROFESOR: ' + profesor_clase.nombre.upper():^60}")
print("=" * 65)
print(f"{'DNI':<12} | {'APELLIDOS, NOMBRE':<25} | {'MEDIA':<7} | {'CRÉDITOS'}")
print("-" * 65)

# Iteramos sobre la lista de alumnos que tiene el profesor
for alumno in profesor_clase.alumnos:
    # Obtenemos los datos calculados mediante los métodos de la clase Alumno
    nota_media = alumno.getNotaMedia()
    creditos_totales = alumno.getNumeroCreditosSuperados()
    nombre_formateado = f"{alumno.apellidos}, {alumno.nombre}"
    
    # Imprimimos la fila con formato para que las columnas queden alineadas
    print(f"{alumno.dni:<12} | {nombre_formateado:<25} | {nota_media:<7.2f} | {creditos_totales:>8}")

print("-" * 65)
print(f"Total de alumnos gestionados: {len(profesor_clase.alumnos)}")
            
               








