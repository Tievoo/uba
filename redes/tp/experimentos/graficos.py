"""Genera los gráficos del experimento 1 a partir de resultados/exp1.json."""
import json
import statistics
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from corrida import RESULTADOS

AZUL, NARANJA, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
TEXTO, MUTED, GRID, FONDO = "#0b0b0b", "#52514e", "#e1e0d9", "#fcfcfb"

plt.rcParams.update({
    "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": TEXTO, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": FONDO,
    "axes.facecolor": FONDO, "lines.linewidth": 2, "lines.solid_capstyle": "round",
})

d = json.loads((RESULTADOS / "exp1.json").read_text(encoding="utf-8"))
P = d["parametros"]
R, DELAY = P["rate"], P["delay"]
L, F, ACK = 256 * 8, 263 * 8, 4 * 8
T_TX = F / R
RTT = 2 * DELAY + ACK / R


def kbps(x):
    return x / 1e3


# ------------------------------------------------------------- Parte A
por_w = defaultdict(list)
saw = []
for f in d["ventana"]:
    if not f["goodput_bps"]:
        continue
    if f["protocolo"] == "stopandwait":
        saw.append(f["goodput_bps"])
    else:
        por_w[f["window_size"]].append(f["goodput_bps"])
ws = sorted(por_w)
med = [statistics.mean(por_w[w]) for w in ws]
lo = [statistics.mean(por_w[w]) - min(por_w[w]) for w in ws]
hi = [max(por_w[w]) - statistics.mean(por_w[w]) for w in ws]

# RTT efectivo: lo que realmente tarda un ciclo frame+ack medido con S&W (incluye overhead de Python)
t_ciclo_saw = L / statistics.mean(saw)
teo = [min(w * L / (T_TX + RTT), R * L / F) for w in range(1, 65)]
teo_ef = [min(w * L / t_ciclo_saw, R * L / F) for w in range(1, 65)]

fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(range(1, 65), [kbps(x) for x in teo], color=MUTED, linewidth=1.5,
        label=f"Teórico: min(W·L/(T_tx+RTT), R·L/F), RTT={RTT * 1e3:.1f} ms")
ax.plot(range(1, 65), [kbps(x) for x in teo_ef], color=AQUA,
        label=f"Teórico con ciclo medido en S&W ({t_ciclo_saw * 1e3:.1f} ms)")
ax.errorbar(ws, [kbps(x) for x in med], yerr=[[kbps(x) for x in lo], [kbps(x) for x in hi]], fmt="o",
            color=AZUL, ms=6, mec=FONDO, mew=1.5, capsize=3, linewidth=1.5, label="Sliding window medido (media, mín–máx)")
ax.plot([1], [kbps(statistics.mean(saw))], "s", color=NARANJA, ms=8, mec=FONDO, mew=1.5,
        label="Stop and wait medido")
ax.axvline((T_TX + RTT) / T_TX, color=GRID, linewidth=1)
ax.annotate(f"BDP ≈ {(T_TX + RTT) / T_TX:.0f} frames", ((T_TX + RTT) / T_TX, kbps(R * L / F) * 0.35),
            xytext=(4, 0), textcoords="offset points", color=MUTED, fontsize=9)
ax.set_xlabel("Tamaño de ventana W (frames)")
ax.set_ylabel("Goodput (kbit/s)")
ax.set_title("Goodput vs. tamaño de ventana (2 Mbit/s, RTT 20 ms, sin pérdidas)", loc="left", color=TEXTO, fontsize=11)
ax.set_ylim(0, kbps(R) * 1.05)
ax.set_xlim(0, 66)
ax.legend(frameon=False, fontsize=8.5, loc="lower right")
fig.tight_layout()
fig.savefig(RESULTADOS / "exp1_ventana.png", dpi=180)

# ------------------------------------------------------------- Parte B
series = defaultdict(lambda: defaultdict(list))
for f in d["perdidas"]:
    clave = "Stop and wait" if f["protocolo"] == "stopandwait" else f"Sliding window W={f['window_size']}"
    if f["goodput_bps"]:
        series[clave][f["canal_loss"]].append(f["goodput_bps"])
fig, ax = plt.subplots(figsize=(7.2, 4.2))
for (nombre, color) in (("Sliding window W=32", AZUL), ("Sliding window W=8", AQUA), ("Stop and wait", NARANJA)):
    ps = sorted(series[nombre])
    ys = [kbps(statistics.mean(series[nombre][p])) for p in ps]
    ax.plot([p * 100 for p in ps], ys, "-o", color=color, ms=6, mec=FONDO, mew=1.5, label=nombre)
    ax.annotate(nombre, (ps[-1] * 100, ys[-1]), xytext=(6, 0), textcoords="offset points", va="center",
                color=TEXTO, fontsize=8.5)
ax.set_xlabel("Probabilidad de pérdida por frame, en cada sentido (%)")
ax.set_ylabel("Goodput (kbit/s)")
ax.set_title("Goodput vs. pérdidas (timeout 100 ms, RTT 20 ms)", loc="left", color=TEXTO, fontsize=11)
ax.set_ylim(bottom=0)
ax.set_xlim(-0.3, 12.5)
ax.legend(frameon=False, fontsize=8.5)
fig.tight_layout()
fig.savefig(RESULTADOS / "exp1_perdidas.png", dpi=180)

resumen = {"t_tx_ms": T_TX * 1e3, "rtt_ms": RTT * 1e3, "ciclo_saw_ms": t_ciclo_saw * 1e3,
           "saw_kbps": kbps(statistics.mean(saw)),
           "ventana": {w: {"medido_kbps": kbps(m), "teorico_kbps": kbps(min(w * L / (T_TX + RTT), R * L / F)),
                           "teorico_ef_kbps": kbps(min(w * L / t_ciclo_saw, R * L / F))} for w, m in zip(ws, med)},
           "perdidas": {n: {p: kbps(statistics.mean(v)) for p, v in sorted(s.items())} for n, s in series.items()}}
(RESULTADOS / "exp1_resumen.json").write_text(json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(resumen, indent=2, ensure_ascii=False))
