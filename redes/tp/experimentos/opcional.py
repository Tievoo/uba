"""
Ejercicios opcionales (sección 2.4):
  (a) variar CHUNK_SIZE y ver el BMP recibido con el protocolo dumb
  (b) transmitir imágenes PNG / JPEG / GIF con el protocolo dumb

tux.bmp: 265 x 314 píxeles, 32 bits por píxel -> cada fila ocupa 1060 bytes,
y los píxeles empiezan en el byte 138 (header BMP v5).

Uso: python opcional.py -> resultados/opcional.json, resultados/opc_*.png
"""
import shutil
from PIL import Image
from corrida import RESULTADOS, TUX, comparar, correr, guardar_json
from imagenes import mosaico

IMG = RESULTADOS / "img"
IMG.mkdir(exist_ok=True)
TMP = RESULTADOS / "tmp"
TMP.mkdir(exist_ok=True)
res = {"chunk_size": [], "formatos": []}

# ---------------------------------------------------------------- (a) CHUNK_SIZE
# 64, 256: múltiplos de 4 (1 píxel = 4 bytes) pero no de 1060 (una fila)
# 255, 1061: NO son múltiplos de 4 -> al perder un chunk se corren los canales de color
# 1060, 4240: exactamente 1 y 4 filas
CHUNKS = [64, 256, 255, 1060, 1061, 4240]
items = [(TUX, "Original", "")]
for cs in CHUNKS:
    # Usamos una pérdida tal que se pierdan ~6 frames en promedio para todos
    # los tamaños, para que las imágenes sean comparables
    frames = -(-TUX.stat().st_size // cs)
    loss = 6 / frames
    r = correr("dumb", servidor={"loss": round(loss, 5), "seed": 7}, chunk_size=cs, limite=60)
    perdidos = frames - (r["bytes_recibido"] + cs - 1) // cs
    fila = {"chunk_size": cs, "frames": frames, "loss": loss, "multiplo_de_4": cs % 4 == 0,
            "filas_por_chunk": cs / 1060, **{k: r.get(k) for k in ("bytes_recibido", "chunks_distintos", "servidor_colgado")}}
    res["chunk_size"].append(fila)
    print(fila, flush=True)
    dst = IMG / f"opc_chunk{cs}.bmp"
    shutil.copy(r["salida"], dst)
    items.append((dst, f"CHUNK_SIZE = {cs}", f"{frames} frames, recibidos {r['bytes_recibido']} B"))
mosaico(items, RESULTADOS / "opc_chunk_size.png", columnas=4)

# ---------------------------------------------------------------- (b) otros formatos
tux = Image.open(TUX).convert("RGBA")
fuentes = {
    "png": TMP / "tux.png",
    "jpg": TMP / "tux.jpg",
    "gif": TMP / "tux.gif",
}
fondo = Image.new("RGB", tux.size, "white")
fondo.paste(tux, mask=tux.split()[3])
fondo.save(fuentes["png"])
fondo.save(fuentes["jpg"], quality=90)
fondo.save(fuentes["gif"])

items = []
for fmt, src in fuentes.items():
    items.append((src, f"{fmt.upper()} original", f"{src.stat().st_size} bytes"))
    for seed in (3, 11):
        frames = -(-src.stat().st_size // 256)
        r = correr("dumb", archivo=src, servidor={"loss": 0.03, "seed": seed}, limite=60)
        dst = IMG / f"opc_{fmt}_seed{seed}{src.suffix}"
        shutil.copy(r["salida"], dst)
        fila = {"formato": fmt, "seed": seed, "frames": frames, "bytes_original": src.stat().st_size,
                **{k: r.get(k) for k in ("bytes_recibido", "chunks_distintos", "identico", "servidor_colgado")}}
        res["formatos"].append(fila)
        print(fila, flush=True)
        items.append((dst, f"{fmt.upper()} por dumb, 3% (seed {seed})",
                      f"{r['bytes_recibido']}/{src.stat().st_size} bytes"))
mosaico(items, RESULTADOS / "opc_formatos.png", columnas=3)

guardar_json("opcional.json", res)
print("listo")
