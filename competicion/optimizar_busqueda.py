"""
OPTIMIZADOR ULTRA-RÁPIDO — CONCURSO ML
Estrategia clave:
  1. Precomputar matriz de distancias UNA VEZ por (normalizer × dist_type)
  2. Barrer TODOS los k = 1..30 en un ÚNICO paso sobre esa matriz
  3. Explorar: euclídea, manhattan, ponderada (Pearson / Relief + variantes)
Validación Cruzada 5 SIN SHUFFLE  |  Coste: O(n_norm × n_dist × n²)
"""

import sys, os, math, time
sys.path.insert(0, '/home/claude')
os.chdir('/home/claude')

from factorias import FactoriaCSV
from procesado import NormalizadorMaxMin, NormalizadorZ_Score
from validacion import SeleccionAtributos

# ─────────────────────────── HELPERS ────────────────────────────────

def apply_norm(ds, name):
    if name == "MaxMin":
        n = NormalizadorMaxMin(); n.ajustar(ds); return n.transformar_dataSet(ds)
    if name == "ZScore":
        n = NormalizadorZ_Score(); n.ajustar(ds); return n.transformar_dataSet(ds)
    return ds

def make_matrix(recs, dist, w=None):
    n = len(recs)
    atrs = [r.atributos for r in recs]
    mat = [[0.0]*n for _ in range(n)]
    for i in range(n):
        ai = atrs[i]
        for j in range(i+1, n):
            aj = atrs[j]
            if dist == "euclídea":
                d = math.sqrt(sum((a-b)**2 for a,b in zip(ai,aj)))
            elif dist == "manhattan":
                d = sum(abs(a-b) for a,b in zip(ai,aj))
            else:
                d = math.sqrt(sum(wi*(a-b)**2 for wi,a,b in zip(w,ai,aj)))
            mat[i][j] = mat[j][i] = d
    return mat

# ─────────────────────────── REGRESIÓN ──────────────────────────────

def sweep_regression(recs, mat, ks, m=5):
    n = len(recs); sz = n//m
    objs = [r.objetivo for r in recs]
    maxk = max(ks); ks_set = set(ks)
    acc = {k:[0.0,0.0,0] for k in ks}          # [sq_err, abs_err, count]

    for fold in range(m):
        ini = fold*sz; fin = (fold+1)*sz if fold!=m-1 else n
        train = list(range(0,ini))+list(range(fin,n))
        for ti in range(ini, fin):
            row = mat[ti]
            sorted_tr = sorted((row[t],t) for t in train)
            real = objs[ti]; run = 0.0
            for rank,(_, tri) in enumerate(sorted_tr[:maxk]):
                run += objs[tri]; k = rank+1
                if k in ks_set:
                    e = run/k - real
                    acc[k][0]+=e*e; acc[k][1]+=abs(e); acc[k][2]+=1

    out = {}
    for k,(sq,ab,cnt) in acc.items():
        if cnt:
            mse=sq/cnt; out[k]={"MSE":mse,"RMSE":math.sqrt(mse),"MAE":ab/cnt}
    return out

# ─────────────────────────── CLASIFICACIÓN ──────────────────────────

def sweep_classification(recs, mat, ks, m=5):
    n = len(recs); sz = n//m
    objs = [r.objetivo for r in recs]
    maxk = max(ks); ks_set = set(ks)
    pairs = {k:[] for k in ks}

    for fold in range(m):
        ini = fold*sz; fin = (fold+1)*sz if fold!=m-1 else n
        train = list(range(0,ini))+list(range(fin,n))
        for ti in range(ini, fin):
            row = mat[ti]
            sorted_tr = sorted((row[t],t) for t in train)
            real = objs[ti]; votes={}
            for rank,(_,tri) in enumerate(sorted_tr[:maxk]):
                lbl=objs[tri]; votes[lbl]=votes.get(lbl,0)+1; k=rank+1
                if k in ks_set:
                    pairs[k].append((max(votes,key=votes.get), real))

    out = {}
    for k,ps in pairs.items():
        if not ps: continue
        nt=len(ps); correct=sum(1 for p,r in ps if p==r)
        acc=correct/nt*100
        clases=set(r for _,r in ps)
        tp_fp_fn={c:[0,0,0] for c in clases}
        for p,r in ps:
            if p==r: tp_fp_fn[r][0]+=1
            else:   tp_fp_fn[p][1]+=1; tp_fp_fn[r][2]+=1
        pr=re=0.0
        for c,(tp,fp,fn) in tp_fp_fn.items():
            pr+=tp/(tp+fp) if tp+fp else 0; re+=tp/(tp+fn) if tp+fn else 0
        pr=pr/len(clases)*100; re=re/len(clases)*100
        f1=2*pr*re/(pr+re) if pr+re else 0
        out[k]={"Accuracy":acc,"F1":f1,"Precision":pr,"Recall":re}
    return out

# ─────────────────────────── BÚSQUEDA COMPLETA ─────────────────────

def search(ds_raw, mode, label):
    print(f"\n{'='*65}\n  {label}\n{'='*65}")
    t0g=time.time()
    n=len(ds_raw.registros)
    print(f"  {n} registros | {len(ds_raw.registros[0].atributos)} atributos")

    KS = list(range(1,31))
    norms = ["Sin normalizar","MaxMin","ZScore"]
    best_key = "MSE" if mode=="reg" else "Accuracy"
    best_val = float("inf") if mode=="reg" else -1.0
    best_cfg = None; all_res = []

    for norm_name in norms:
        t0=time.time()
        ds = apply_norm(ds_raw, norm_name)
        recs = ds.registros

        if mode=="reg":
            raw_w = SeleccionAtributos.calcular_pesos_pearson(ds)
        else:
            raw_w = SeleccionAtributos.calcular_pesos_relief(ds, iteraciones=100)

        # Variantes de pesos
        w_thresh = [w if w>0.1 else 0.0 for w in raw_w]
        w_sq     = [w**2 for w in raw_w]
        w_sqrt   = [math.sqrt(w) for w in raw_w]

        dist_cfgs = [
            ("euclídea",  None,     "—"),
            ("manhattan", None,     "—"),
            ("ponderada", raw_w,    "pearson/relief"),
            ("ponderada", w_thresh, "thresh>0.1"),
            ("ponderada", w_sq,     "cuadrado"),
            ("ponderada", w_sqrt,   "raíz"),
        ]

        for dist_name, weights, ptag in dist_cfgs:
            mat = make_matrix(recs, dist_name, weights)
            res = sweep_regression(recs,mat,KS) if mode=="reg" else sweep_classification(recs,mat,KS)

            for k, metrics in res.items():
                cfg = {"k":k,"norm":norm_name,"dist":dist_name,"pesos":ptag,**metrics}
                all_res.append(cfg)
                val = metrics[best_key]
                better = (val < best_val) if mode=="reg" else (val > best_val)
                if better:
                    best_val=val; best_cfg=cfg
                    tag = f"MSE={val:.4f}  RMSE={metrics['RMSE']:.4f}" if mode=="reg" \
                          else f"Acc={val:.4f}%  F1={metrics['F1']:.4f}%"
                    print(f"  ★  k={k:2d} | {norm_name:14s} | {dist_name:10s} "
                          f"({ptag:16s}) → {tag}")

        print(f"     [{norm_name}] {time.time()-t0:.1f}s")

    print(f"\n  Tiempo total: {time.time()-t0g:.1f}s")
    return best_cfg, all_res


# ─────────────────────────── MAIN ───────────────────────────────────

if __name__=="__main__":
    print("\n"+"*"*65)
    print("  CONCURSO ML — OPTIMIZADOR ULTRA-RÁPIDO (matrices precalculadas)")
    print("*"*65)

    ds_reg  = FactoriaCSV.crear_dataset_regresion("/home/claude/Concrete_Data.csv", indice_objetivo=-1)
    ds_clas = FactoriaCSV.crear_dataset_clasificacion("/home/claude/wdbc.csv", indice_objetivo=-1)

    best_reg,  all_reg  = search(ds_reg,  "reg",  "CONCRETE — Regresión kNN")
    best_clas, all_clas = search(ds_clas, "clas", "WDBC — Clasificación kNN")

    # ── TOP 10 ──
    print("\n"+"="*65+"\n  TOP 10 — CONCRETE (menor MSE)\n"+"="*65)
    for i,c in enumerate(sorted(all_reg,  key=lambda x: x["MSE"])[:10], 1):
        print(f"  {i:2d}. k={c['k']:2d} | {c['norm']:14s} | {c['dist']:10s} ({c['pesos']:16s})"
              f"  MSE={c['MSE']:8.3f}  RMSE={c['RMSE']:6.3f}")

    print("\n"+"="*65+"\n  TOP 10 — WDBC (mayor Accuracy)\n"+"="*65)
    for i,c in enumerate(sorted(all_clas, key=lambda x: -x["Accuracy"])[:10], 1):
        print(f"  {i:2d}. k={c['k']:2d} | {c['norm']:14s} | {c['dist']:10s} ({c['pesos']:16s})"
              f"  Acc={c['Accuracy']:7.4f}%  F1={c['F1']:7.4f}%")

    print("\n"+"="*65+"\n  🏆  GANADOR — CONCRETE\n"+"="*65)
    c=best_reg
    print(f"  k={c['k']} | norm={c['norm']} | dist={c['dist']} ({c['pesos']})")
    print(f"  MSE={c['MSE']:.6f}  RMSE={c['RMSE']:.6f}  MAE={c['MAE']:.6f}")

    print("\n"+"="*65+"\n  🏆  GANADOR — WDBC\n"+"="*65)
    c=best_clas
    print(f"  k={c['k']} | norm={c['norm']} | dist={c['dist']} ({c['pesos']})")
    print(f"  Accuracy={c['Accuracy']:.6f}%  F1={c['F1']:.6f}%")
    print(f"  Precision={c['Precision']:.6f}%  Recall={c['Recall']:.6f}%")

    print("\n"+"*"*65+"\n  FIN\n"+"*"*65)
