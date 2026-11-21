"""Helpers para visualizar los BMP recibidos (aunque estén truncados o rotos)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFile, ImageFont

ImageFile.LOAD_TRUNCATED_IMAGES = True


def abrir(path):
    """Abre una imagen recibida. Devuelve (imagen RGB o None, mensaje de error)."""
    try:
        im = Image.open(path)
        im.load()
        return im.convert("RGB"), None
    except Exception as e:  # header roto, formato irreconocible, etc.
        return None, f"{type(e).__name__}: {e}"[:80]


def _font(size):
    for name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def mosaico(items, destino, columnas=4, ancho=265, alto=314):
    """items: lista de (path_imagen, titulo, subtitulo). Arma una grilla PNG."""
    titulo_h = 48
    filas = (len(items) + columnas - 1) // columnas
    hoja = Image.new("RGB", (columnas * (ancho + 16) + 16, filas * (alto + titulo_h + 16) + 16), "white")
    d = ImageDraw.Draw(hoja)
    f1, f2 = _font(15), _font(12)
    for k, (path, titulo, sub) in enumerate(items):
        x = 16 + (k % columnas) * (ancho + 16)
        y = 16 + (k // columnas) * (alto + titulo_h + 16)
        d.text((x, y), titulo, fill="black", font=f1)
        d.text((x, y + 20), sub, fill="#555555", font=f2)
        im, err = abrir(path)
        y += titulo_h
        if im is None:
            d.rectangle([x, y, x + ancho, y + alto], outline="#cc0000", width=2)
            d.multiline_text((x + 8, y + 8), "No se puede abrir:\n" + "\n".join(err[i:i + 32] for i in range(0, len(err), 32)),
                             fill="#cc0000", font=f2)
        else:
            im.thumbnail((ancho, alto))
            hoja.paste(im, (x, y))
            d.rectangle([x - 1, y - 1, x + im.width, y + im.height], outline="#bbbbbb")
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    hoja.save(destino)
    return destino
