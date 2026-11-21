"""
Ejercicios obligatorios del taller 2 (secciones 2.1, 2.2 y 2.3).

Uso:  python ejercicios.py
Genera resultados/ejercicios.json y las imágenes resultados/ej_*.png
"""
import shutil
from corrida import AQUI, RESULTADOS, TUX, correr, guardar_json
from imagenes import mosaico

IMG = RESULTADOS / "img"
IMG.mkdir(exist_ok=True)
ORIGINAL = AQUI / "original"
SEMILLAS = [1, 2, 3]

res = {}


def resumen(r):
    return {k: r.get(k) for k in ("tiempo", "enviados", "retransmisiones", "identico", "bytes_original",
                                  "bytes_recibido", "chunks_distintos", "colgado", "servidor_colgado", "canal")}


def guardar_img(r, nombre):
    dst = IMG / nombre
    shutil.copy(r["salida"], dst)
    return dst


# ---------------------------------------------------------------- 2.1 dumb
print("2.1 dumb")
res["2.1_dumb_loss1%"] = []
items = [(TUX, "Original", "tux.bmp, 332978 bytes")]
for s in SEMILLAS:
    r = correr("dumb", servidor={"loss": 0.01, "seed": s}, limite=60)
    res["2.1_dumb_loss1%"].append(resumen(r))
    p = guardar_img(r, f"dumb_loss1_seed{s}.bmp")
    items.append((p, f"dumb, 1% pérdida (seed {s})", f"{r['bytes_recibido']} bytes, {r['chunks_distintos']} chunks mal"))
mosaico(items, RESULTADOS / "ej_2_1_dumb.png")

# 2.1d: condiciones del canal. (1) sin pérdidas -> funciona
r = correr("dumb", servidor={"loss": 0, "seed": 1}, limite=60)
res["2.1d_dumb_sin_perdidas"] = resumen(r)
# (2) sin pérdidas pero con reordenamiento: mismo tamaño, contenido distinto
r = correr("dumb", servidor={"loss": 0},
           canal={"delay": 0.001, "late_prob": 0.01, "late_delay": 0.01, "seed": 1, "idle_exit": 1}, limite=60)
res["2.1d_dumb_reordenamiento"] = resumen(r)
p1 = guardar_img(r, "dumb_reorden.bmp")
mosaico([(TUX, "Original", ""),
         (IMG / "dumb_loss1_seed1.bmp", "dumb, 1% pérdida", "se pierden chunks"),
         (p1, "dumb, 0% pérdida + reordenamiento", f"{r['bytes_recibido']} bytes, {r['chunks_distintos']} chunks mal")],
        RESULTADOS / "ej_2_1d_condiciones.png", columnas=3)

# ---------------------------------------------------------------- 2.2a stop and wait original
print("2.2a stop and wait original (sin número de secuencia)")
res["2.2a_saw_original_loss1%"] = []
items = [(TUX, "Original", "")]
for s in SEMILLAS:
    r = correr("stopandwait", servidor={"loss": 0.01, "seed": s}, directorio=ORIGINAL, limite=120)
    res["2.2a_saw_original_loss1%"].append(resumen(r))
    p = guardar_img(r, f"saw_original_seed{s}.bmp")
    items.append((p, f"S&W original, 1% pérdida (seed {s})", f"{r['bytes_recibido']} bytes, {r['chunks_distintos']} chunks mal"))
mosaico(items, RESULTADOS / "ej_2_2a_saw_original.png")
r = correr("stopandwait", servidor={"loss": 0, "seed": 1}, directorio=ORIGINAL, limite=120)
res["2.2a_saw_original_sin_perdidas"] = resumen(r)

# ---------------------------------------------------------------- 2.2c stop and wait con bit alternante
print("2.2c stop and wait con número de secuencia")
res["2.2c_saw_modificado_loss1%"] = []
for s in SEMILLAS:
    r = correr("stopandwait", servidor={"loss": 0.01, "seed": s}, limite=120)
    res["2.2c_saw_modificado_loss1%"].append(resumen(r))
res["2.2c_saw_modificado_loss10%"] = resumen(correr("stopandwait", servidor={"loss": 0.10, "seed": 1}, limite=300))

# ---------------------------------------------------------------- 2.3c sliding window
print("2.3c sliding window")
res["2.3c_sw_loss1%"] = []
for s in SEMILLAS:
    r = correr("slidingwindow", servidor={"loss": 0.01, "seed": s}, limite=120)
    res["2.3c_sw_loss1%"].append(resumen(r))
res["2.3c_sw_loss10%"] = resumen(correr("slidingwindow", servidor={"loss": 0.10, "seed": 1}, limite=300))

guardar_json("ejercicios.json", res)
for k, v in res.items():
    for x in (v if isinstance(v, list) else [v]):
        print(f"{k:32s} identico={x['identico']!s:5s} bytes={x['bytes_recibido']:6d} "
              f"chunks_mal={x['chunks_distintos']:4d} t={x['tiempo']} retx={x['retransmisiones']} colgado={x['colgado']}")
