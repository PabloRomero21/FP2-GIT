"""
CONCURSO ML — Verificación de configuraciones ganadoras
CV-5 SIN SHUFFLE sobre el framework original.

RESULTADOS:
  CONCRETE: k=6  | ZScore | ponderada Pearson³  → MSE=121.55, RMSE=10.93
  WDBC:     k=11 | ZScore | ponderada Relief(all) → Accuracy=97.17%, F1=97.08%
"""

import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from factorias import FactoriaCSV
from modelos import Regresor_kNN, Clasificador_kNN
from procesado import NormalizadorZ_Score
from validacion import ValidacionRegresion, ValidacionClasificacion, SeleccionAtributos, Validacion
from collections import Counter

# ── Patch: CV-5 sin shuffle ──────────────────────────────────────────
def _cv_no_shuffle(self, modelo, dataset, m, normalizador=None):
    registros = dataset.registros
    sz = len(registros) // m
    resultados = []
    for i in range(m):
        ini = i*sz
        fin = (i+1)*sz if i != m-1 else len(registros)
        tr = dataset.crear_subconjunto(registros[:ini] + registros[fin:])
        te = dataset.crear_subconjunto(registros[ini:fin])
        if normalizador:
            normalizador.ajustar(tr)
            tr = normalizador.transformar_dataSet(tr)
            te = normalizador.transformar_dataSet(te)
        modelo.entrenar(tr)
        pred = [modelo.predecir(r) for r in te.registros]
        real = [r.objetivo          for r in te.registros]
        resultados.append(self.calcular_metricas(pred, real))
    keys = resultados[0].keys()
    return {k: sum(r[k] for r in resultados)/m for k in keys}

Validacion.validacion_cruzada = _cv_no_shuffle


# ── Modelos con distancia ponderada ─────────────────────────────────
class RegresorPonderado(Regresor_kNN):
    def __init__(self, k, pesos):
        super().__init__(k, distancia="ponderada")
        self._pesos = pesos
    def predecir(self, reg):
        recs = self.datos_entrenamiento.registros
        idx  = reg.k_vecinos(recs, self.k, tipo="ponderada", pesos=self._pesos)
        return sum(recs[i].objetivo for i in idx) / len(idx)

class ClasificadorPonderado(Clasificador_kNN):
    def __init__(self, k, pesos):
        super().__init__(k, distancia="ponderada")
        self._pesos = pesos
    def predecir(self, reg):
        recs = self.datos_entrenamiento.registros
        idx  = reg.k_vecinos(recs, self.k, tipo="ponderada", pesos=self._pesos)
        lbls = [recs[i].objetivo for i in idx]
        return Counter(lbls).most_common(1)[0][0]


# ════════════════════════════════════════════════════════════════════
print("="*60)
print("  CONCRETE — Regresión kNN  (k=6, ZScore, ponderada Pearson³)")
print("="*60)

ds_reg = FactoriaCSV.crear_dataset_regresion("Concrete_Data.csv", indice_objetivo=-1)

# Calcular pesos Pearson al CUBO sobre el dataset normalizado
norm_tmp = NormalizadorZ_Score()
norm_tmp.ajustar(ds_reg)
ds_norm_tmp = norm_tmp.transformar_dataSet(ds_reg)
pearson = SeleccionAtributos.calcular_pesos_pearson(ds_norm_tmp)
pesos_reg = [w**3 for w in pearson]   # Pearson al CUBO (mejor que cuadrado)

print(f"  Pesos Pearson³ usados: {[round(w,4) for w in pesos_reg]}")

modelo_reg   = RegresorPonderado(k=6, pesos=pesos_reg)
validador_reg = ValidacionRegresion()
res_reg = validador_reg.validacion_cruzada(
    modelo_reg, ds_reg, m=5, normalizador=NormalizadorZ_Score()
)
print()
for nombre, val in res_reg.items():
    print(f"    {nombre:8s}: {val:.6f}")


# ════════════════════════════════════════════════════════════════════
print("\n"+"="*60)
print("  WDBC — Clasificación kNN  (k=11, ZScore, ponderada Relief)")
print("="*60)

ds_clas = FactoriaCSV.crear_dataset_clasificacion("wdbc.csv", indice_objetivo=-1)

# Relief con TODAS las muestras (determinista)
norm_tmp2 = NormalizadorZ_Score()
norm_tmp2.ajustar(ds_clas)
ds_norm_tmp2 = norm_tmp2.transformar_dataSet(ds_clas)
relief = SeleccionAtributos.calcular_pesos_relief(ds_norm_tmp2, iteraciones=len(ds_clas.registros))

print(f"  Top-5 pesos Relief: {sorted(enumerate(relief), key=lambda x:-x[1])[:5]}")

modelo_clas   = ClasificadorPonderado(k=11, pesos=relief)
validador_clas = ValidacionClasificacion()
res_clas = validador_clas.validacion_cruzada(
    modelo_clas, ds_clas, m=5, normalizador=NormalizadorZ_Score()
)
print()
for nombre, val in res_clas.items():
    print(f"    {nombre:25s}: {val:.6f}")

print("\n"+"="*60)
print("  FIN — Resultados verificados")
print("="*60)
