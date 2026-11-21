"""
Experimento 3: espacio de números de secuencia finito en sliding window.

Si los números de secuencia van módulo N y el receptor tiene RWS = 1, el
protocolo es correcto sólo si SWS <= N - 1 (en general, SWS + RWS <= N).
Con N = 8 probamos SWS en {4, 7, 8, 12} bajo tres canales:

  1) ideal: sin pérdidas, retardo 5 ms
  2) pérdidas aleatorias: 5% en cada sentido
  3) ráfagas de pérdida de acks: con prob. 2% por ack se pierden 12 acks
     seguidos (sólo en el sentido servidor -> cliente)

Uso: python exp3_espacio_secuencia.py -> resultados/exp3.json, resultados/exp3_imagenes.png
"""
import shutil
from corrida import AQUI, RESULTADOS, TUX, correr, guardar_json
from imagenes import mosaico

MODN = AQUI / "modn"
IMG = RESULTADOS / "img"
IMG.mkdir(exist_ok=True)
N = 8
VENTANAS = [4, 7, 8, 12]
CANALES = {
    "1_ideal": {"delay": 0.005},
    "2_perdidas_5%": {"delay": 0.005, "loss": 0.05},
    "3_rafagas_acks": {"delay": 0.005, "burst_prob": 0.02, "burst_len": 12, "dirs": "rev"},
}
SEMILLAS = [1, 2, 3]
res = []
imgs = [(TUX, "Original", "")]

for nombre, canal in CANALES.items():
    for sws in VENTANAS:
        for seed in SEMILLAS:
            r = correr("modn", cliente={"timeout": 0.1, "window_size": sws, "max_seq": N},
                       servidor={"max_seq": N, "linger": 1}, canal={**canal, "seed": seed, "idle_exit": 1},
                       cliente_script=MODN / "slidingwindow_client_send.py",
                       servidor_script=MODN / "slidingwindow_server_recv.py", limite=90)
            fila = {"canal": nombre, "sws": sws, "N": N, "seed": seed,
                    **{k: r.get(k) for k in ("tiempo", "retransmisiones", "identico", "bytes_recibido",
                                             "chunks_distintos", "colgado", "canal")}}
            res.append(fila)
            print(f"{nombre:16s} SWS={sws:2d} seed={seed} ok={fila['identico']!s:5s} chunks_mal={fila['chunks_distintos']:4d} "
                  f"bytes={fila['bytes_recibido']} t={fila['tiempo']} colgado={fila['colgado']} canal={fila['canal']}",
                  flush=True)
            if nombre.startswith("3") and seed == 1:
                dst = IMG / f"exp3_sws{sws}.bmp"
                shutil.copy(r["salida"], dst)
                imgs.append((dst, f"SWS={sws}, N={N}, ráfagas de acks",
                             "colgado" if fila["colgado"] else f"{fila['chunks_distintos']} chunks incorrectos"))
        guardar_json("exp3.json", res)

mosaico(imgs, RESULTADOS / "exp3_imagenes.png", columnas=5)
print("listo")
