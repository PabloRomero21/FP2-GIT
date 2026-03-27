import warnings
import pandas as pd

from provincia import Provincia
from comunidad_autonoma import ComunidadAutonoma
from partido import Partido
from pais import Pais


class FabricaElecciones:

    def __init__(self, ruta_xlsx, modo_estricto=False):
        self.ruta_xlsx     = ruta_xlsx
        self.modo_estricto = modo_estricto
        self.errores       = []

    def construir(self):
        df = pd.read_excel(self.ruta_xlsx, sheet_name="Circunscripciones", header=None)

        # Localizar las filas clave buscando textos conocidos
        fila_cabecera  = self._buscar_fila(df, "Nombre de Comunidad")
        fila_partidos  = self._buscar_fila(df, "PARTIDO POPULAR")
        fila_datos     = fila_cabecera + 1

        # Mapear cada campo a su índice de columna
        cab = df.iloc[fila_cabecera]
        col = {texto: int(cab[cab == texto].index[0]) for texto in [
            "Nombre de Comunidad", "Código de Provincia", "Nombre de Provincia",
            "Población", "Número de mesas", "Censo electoral sin CERA",
            "Censo CERA", "Total censo electoral", "Total votantes CER",
            "Total votantes CERA", "Total votantes", "Votos válidos",
            "Votos a candidaturas", "Votos en blanco", "Votos nulos",
        ]}

        # Leer nombres de partidos (cada partido ocupa columna Votos + Diputados)
        inicio_partidos = max(col.values()) + 1
        fila_p = df.iloc[fila_partidos]
        nombres_partidos = []
        c = inicio_partidos
        while c < len(fila_p) and not pd.isna(fila_p[c]):
            nombres_partidos.append(str(fila_p[c]).strip())
            c += 2

        # Recorrer filas de datos construyendo los objetos
        comunidades = {}   # nombre -> ComunidadAutonoma
        partidos    = {}   # nombre -> Partido

        for _, fila in df.iloc[fila_datos:].iterrows():
            if pd.isna(fila[col["Nombre de Comunidad"]]):
                continue  # fila de totales o vacía

            nombre_com  = str(fila[col["Nombre de Comunidad"]]).strip()
            cod_prov    = int(fila[col["Código de Provincia"]])
            nombre_prov = str(fila[col["Nombre de Provincia"]]).strip()

            censo_sin    = self._entero(fila[col["Censo electoral sin CERA"]])
            censo_cera   = self._entero(fila[col["Censo CERA"]])
            censo_total  = self._entero(fila[col["Total censo electoral"]])
            vot_cer      = self._entero(fila[col["Total votantes CER"]])
            vot_cera     = self._entero(fila[col["Total votantes CERA"]])
            vot_total    = self._entero(fila[col["Total votantes"]])
            validos      = self._entero(fila[col["Votos válidos"]])
            candidaturas = self._entero(fila[col["Votos a candidaturas"]])
            blanco       = self._entero(fila[col["Votos en blanco"]])
            nulos        = self._entero(fila[col["Votos nulos"]])

            ctx = f"[{nombre_com} / {nombre_prov}]"
            self._check(censo_sin + censo_cera == censo_total,
                f"{ctx} Censo sin CERA + Censo CERA ({censo_sin+censo_cera:,}) ≠ Total censo ({censo_total:,})")
            self._check(vot_cer + vot_cera == vot_total,
                f"{ctx} Votantes CER + CERA ({vot_cer+vot_cera:,}) ≠ Total votantes ({vot_total:,})")
            self._check(validos == candidaturas + blanco,
                f"{ctx} Votos válidos ({validos:,}) ≠ Candidaturas + Blanco ({candidaturas+blanco:,})")
            self._check(nulos + validos == vot_total,
                f"{ctx} Nulos + Válidos ({nulos+validos:,}) ≠ Total votantes ({vot_total:,})")

            # Leer resultados de partidos, omitiendo los que tienen 0 votos
            lista_partidos_prov = []
            suma_votos = 0
            c = inicio_partidos
            for nombre_partido in nombres_partidos:
                votos     = self._entero(fila[c])
                diputados = self._entero(fila[c + 1])+
                c += 2
                if votos == 0:
                    continue
                lista_partidos_prov.append((nombre_partido, votos, diputados))
                suma_votos += votos

                if nombre_partido not in partidos:
                    partidos[nombre_partido] = Partido(nombre_partido)
                partidos[nombre_partido].resultados_por_comunidad \
                    .setdefault(nombre_com, {})[nombre_prov] = (votos, diputados)

            self._check(suma_votos == candidaturas,
                f"{ctx} Suma votos partidos ({suma_votos:,}) ≠ Votos candidaturas ({candidaturas:,})")

            # Crear provincia y añadirla a su comunidad
            provincia = Provincia(
                nombre_prov, self._entero(fila[col["Población"]]),
                self._entero(fila[col["Número de mesas"]]),
                censo_sin, censo_cera, censo_total,
                vot_cer, vot_cera, vot_total,
                validos, candidaturas, blanco, nulos,
                lista_partidos_prov,
            )

            if nombre_com not in comunidades:
                comunidades[nombre_com] = ComunidadAutonoma(nombre_com)
            comunidades[nombre_com].provincias[cod_prov] = provincia

        # Mostrar resumen
        print(f"Comunidades: {len(comunidades)} | Provincias: {sum(len(c.provincias) for c in comunidades.values())} | Partidos: {len(partidos)} | Errores: {len(self.errores)}")

        return Pais("España", list(comunidades.items()), list(partidos.items()))

    def _buscar_fila(self, df, texto):
        for i, fila in df.iterrows():
            if fila.astype(str).str.contains(texto, regex=False).any():
                return i
        raise ValueError(f"No se encontró la fila con '{texto}'")

    def _entero(self, val):
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return 0
        return int(val)

    def _check(self, condicion, mensaje):
        if not condicion:
            self.errores.append(mensaje)
            if self.modo_estricto:
                raise ValueError(mensaje)
            warnings.warn(f"⚠️ {mensaje}")

