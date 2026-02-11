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
        self.alumnos = alumnos
    
    def set_nota_alumno(self,dni,nota_actualizada):
        for alumno in self.alumnos:
            if alumno.dni == dni:
                for i,(asignatura,nota_actual) in enumerate(alumno.asignaturas):
                    if asignatura.nombre == self.nombre_asignatura:
                        alumno.asignaturas[i] = (asignatura,float(nota_actualizada))
    

        


def cargar_datos():
    # 1. Cargar Asignaturas
    lista_asignaturas = []
    with open('asignaturas.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            asig = Asignatura(row['nombre'], row['creditos'], row['curso'], row['cuatrimestre'])
            lista_asignaturas.append(asig)








