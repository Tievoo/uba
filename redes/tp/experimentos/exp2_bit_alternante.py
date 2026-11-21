"""
Experimento 2: ¿cuándo deja de alcanzar un número de secuencia de 1 bit?

El stop and wait con bit alternante (sección 2.2) es correcto si el canal es
FIFO: puede perder frames o demorarlos (incluso más que el timeout), pero no
reordenarlos. Lo verificamos en tres canales:

  A) Pérdidas (5% en cada sentido), retardo bajo.
  B) Canal FIFO con timeout prematuro: RTT = 20 ms, timeout = 15 ms. Todos los
     frames se retransmiten "de más", pero en orden.
  C) Canal que reordena: 2% de los frames (datos o acks) se demoran 100 ms
     extra, el doble del timeout (50 ms), y llegan después de frames más nuevos.

En cada canal transferimos tux.bmp con stop and wait (1 bit de secuencia) y con
sliding window (32 bits de secuencia), con 3 semillas distintas.

Uso: python exp2_bit_alternante.py -> resultados/exp2.json, resultados/exp2_reorden.png
"""
import shutil
from corrida import RESULTADOS, TUX, correr, guardar_json
from imagenes import mosaico

IMG = RESULTADOS / "img"
IMG.mkdir(exist_ok=True)

CANALES = {
    "A_perdidas": ({"delay": 0.002, "loss": 0.05}, 0.05),
    "B_fifo_timeout_prematuro": ({"delay": 0.010}, 0.015),
    "C_reordenamiento": ({"delay": 0.002, "late_prob": 0.02, "late_delay": 0.100}, 0.05),
}
SEMILLAS = [1, 2, 3]
res = []
imgs = [(TUX, "Original", "")]

for nombre, (canal, timeout) in CANALES.items():
    for seed in SEMILLAS:
        c = {**canal, "seed": seed, "idle_exit": 1}
        for prot, cli in (("stopandwait", {"timeout": timeout}),
                          ("slidingwindow", {"timeout": timeout, "window_size": 8})):
            r = correr(prot, cliente=cli, servidor={"loss": 0, "linger": 1}, canal=c, limite=300)
            fila = {"canal": nombre, "seed": seed, "protocolo": prot, "timeout": timeout,
                    **{k: r.get(k) for k in ("tiempo", "enviados", "retransmisiones", "identico", "bytes_recibido",
                                             "chunks_distintos", "colgado", "canal")}}
            dup = r["log_servidor"].count("duplicado")
            res.append(fila)
            print(f"{nombre:26s} seed={seed} {prot:14s} ok={fila['identico']!s:5s} chunks_mal={fila['chunks_distintos']:4d} "
                  f"bytes={fila['bytes_recibido']} t={fila['tiempo']} retx={fila['retransmisiones']} canal={fila['canal']}",
                  flush=True)
            if nombre.startswith("C") and prot == "stopandwait":
                dst = IMG / f"exp2_saw_reorden_seed{seed}.bmp"
                shutil.copy(r["salida"], dst)
                imgs.append((dst, f"S&W 1 bit, reordenamiento (seed {seed})", f"{fila['chunks_distintos']} chunks incorrectos"))
            if nombre.startswith("C") and prot == "slidingwindow" and seed == 1:
                dst = IMG / "exp2_sw_reorden_seed1.bmp"
                shutil.copy(r["salida"], dst)
                sw_img = (dst, "Sliding window 32 bits (seed 1)", f"{fila['chunks_distintos']} chunks incorrectos")
        guardar_json("exp2.json", res)

mosaico(imgs + [sw_img], RESULTADOS / "exp2_reorden.png", columnas=5)
print("listo")
