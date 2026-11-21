"""
Experimento 1: throughput de stop and wait vs sliding window en un enlace con
retardo y tasa finita (emulado con canal.py).

Enlace: 2 Mbit/s, retardo de propagación 10 ms por sentido (RTT = 20 ms).
Frame de datos: 3+4 bytes de header + 256 de datos = 263 bytes
  -> T_tx = 263*8 / 2e6 = 1.05 ms
  -> producto ancho de banda x retardo = 2e6 * 21.05e-3 = 42100 bits ~ 20 frames

Parte A: tamaño de ventana W en {1, ..., 64}, sin pérdidas.
         Goodput teórico = min(W * L / (T_tx + RTT), R * L / F)
Parte B: probabilidad de pérdida p en ambos sentidos, timeout = 100 ms.

Uso: python exp1_throughput.py  -> resultados/exp1.json
"""
from pathlib import Path
from corrida import RESULTADOS, TUX, correr, guardar_json

DELAY = 0.010
RATE = 2e6
REPS = 3
WINDOWS = [1, 2, 4, 8, 12, 16, 20, 24, 32, 48, 64]
LOSSES = [0.0, 0.01, 0.02, 0.05, 0.10]

# Archivo de prueba: los primeros 128 KiB de tux.bmp (512 frames)
ARCHIVO = RESULTADOS / "tmp" / "tux_128k.bin"
ARCHIVO.parent.mkdir(exist_ok=True)
ARCHIVO.write_bytes(TUX.read_bytes()[:128 * 1024])
DATOS_BITS = 128 * 1024 * 8

canal = {"delay": DELAY, "rate": RATE, "idle_exit": 1}
srv = {"loss": 0, "linger": 1}
res = {"parametros": {"delay": DELAY, "rate": RATE, "archivo_bytes": 128 * 1024, "frames": 512},
       "ventana": [], "perdidas": []}


def medir(protocolo, cliente, canal_opts, etiqueta):
    r = correr(protocolo, archivo=ARCHIVO, cliente=cliente, servidor=srv, canal=canal_opts, limite=300)
    fila = {"etiqueta": etiqueta, "protocolo": protocolo, **cliente, **{f"canal_{k}": v for k, v in canal_opts.items()},
            "tiempo": r.get("tiempo"), "retransmisiones": r.get("retransmisiones"), "identico": r["identico"],
            "goodput_bps": DATOS_BITS / r["tiempo"] if r.get("tiempo") else None}
    print(f"{etiqueta:28s} t={fila['tiempo']}  goodput={fila['goodput_bps'] and fila['goodput_bps'] / 1e3:.0f} kbit/s  "
          f"retx={fila['retransmisiones']}  ok={fila['identico']}", flush=True)
    return fila


# ---------------- Parte A: ventana
for rep in range(REPS):
    res["ventana"].append(medir("stopandwait", {"timeout": 0.5}, canal, f"S&W rep{rep}"))
    for w in WINDOWS:
        res["ventana"].append(medir("slidingwindow", {"timeout": 0.5, "window_size": w}, canal, f"SW W={w} rep{rep}"))
    guardar_json("exp1.json", res)

# ---------------- Parte B: pérdidas
for rep in range(2):
    for p in LOSSES:
        c = {**canal, "loss": p, "seed": 100 + rep}
        res["perdidas"].append(medir("stopandwait", {"timeout": 0.1}, c, f"S&W p={p} rep{rep}"))
        for w in (8, 32):
            res["perdidas"].append(medir("slidingwindow", {"timeout": 0.1, "window_size": w}, c, f"SW W={w} p={p} rep{rep}"))
        guardar_json("exp1.json", res)

print("listo")
