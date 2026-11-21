"""
Utilidades para correr una transferencia (servidor + canal + cliente) y
medir el resultado. Usado por los scripts exp*.py y opcional*.py.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TALLER = (AQUI / "../../talleres/Taller-02-Comunicacion-Confiable").resolve()
RESULTADOS = (AQUI / "../resultados").resolve()
RESULTADOS.mkdir(exist_ok=True)
TUX = TALLER / "tux.bmp"
PY = sys.executable

PUERTOS = {"dumb": 12000, "stopandwait": 12001, "slidingwindow": 12002}
PUERTO_CANAL = 13000


def _args(opts):
    out = []
    for k, v in (opts or {}).items():
        out += [f"--{k.replace('_', '-')}", str(v)]
    return out


def correr(protocolo, archivo=TUX, cliente=None, servidor=None, canal=None,
           chunk_size=None, salida=None, directorio=TALLER, limite=600,
           cliente_script=None, servidor_script=None):
    """Transfiere `archivo` con `protocolo`. Si `canal` no es None, el tráfico
    pasa por canal.py con esas opciones. Devuelve un dict con métricas."""
    env = dict(os.environ)
    if chunk_size:
        env["CHUNK_SIZE"] = str(chunk_size)
    env["PYTHONPATH"] = str(TALLER)
    if salida is None:
        salida = Path(tempfile.mkstemp(suffix=Path(archivo).suffix)[1])
    salida = Path(salida)

    puerto = PUERTOS.get(protocolo, 12003)
    srv_script = servidor_script or (Path(directorio) / f"{protocolo}_server_recv.py")
    cli_script = cliente_script or (Path(directorio) / f"{protocolo}_client_send.py")

    # La salida de los procesos va a archivos temporales: con un PIPE que no se
    # lee hasta el final, el buffer se llena y el servidor se bloquea en print()
    srv_log = tempfile.TemporaryFile(mode="w+", encoding="utf-8", errors="replace")
    srv = subprocess.Popen([PY, str(srv_script), "--file", str(salida), "--port", str(puerto)] + _args(servidor),
                           cwd=TALLER, env=env, stdout=srv_log, stderr=subprocess.STDOUT, text=True)
    can = None
    destino = puerto
    if canal is not None:
        can = subprocess.Popen([PY, str(AQUI / "canal.py"), "--listen-port", str(PUERTO_CANAL),
                                "--server-port", str(puerto)] + _args(canal),
                               env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        destino = PUERTO_CANAL
    time.sleep(0.6)

    t0 = time.perf_counter()
    colgado = False
    try:
        cli = subprocess.run([PY, str(cli_script), "--file", str(archivo), "--port", str(destino)] + _args(cliente),
                             cwd=TALLER, env=env, capture_output=True, text=True, timeout=limite)
        cli_out = cli.stdout + cli.stderr  # (run() lee los pipes mientras corre, no se bloquea)
    except subprocess.TimeoutExpired as e:
        colgado = True
        cli_out = (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
    pared = time.perf_counter() - t0

    def terminar(p, espera):
        try:
            out, _ = p.communicate(timeout=espera)
            return out, False
        except subprocess.TimeoutExpired:
            p.kill()
            out, _ = p.communicate()
            return out, True

    _, srv_colgado = terminar(srv, 8)
    srv_log.seek(0)
    srv_out = srv_log.read()
    srv_log.close()
    can_out = ""
    if can is not None:
        can_out, _ = terminar(can, 8)

    r = {"protocolo": protocolo, "colgado": colgado, "servidor_colgado": srv_colgado, "pared": pared}
    m = re.search(r"terminada en ([\d.]+) s(?: \((\d+) frames enviados, (\d+) retrans)?", cli_out)
    if m:
        r["tiempo"] = float(m.group(1))
        if m.group(2):
            r["enviados"] = int(m.group(2))
            r["retransmisiones"] = int(m.group(3))
    r.update(comparar(archivo, salida, chunk_size or 256))
    if can_out.strip():
        try:
            r["canal"] = json.loads(can_out.strip().splitlines()[-1])
        except json.JSONDecodeError:
            pass
    r["salida"] = str(salida)
    r["log_servidor"] = srv_out[-2000:]
    r["log_cliente"] = cli_out[-2000:]
    return r


def comparar(original, recibido, chunk_size=256):
    a = Path(original).read_bytes()
    b = Path(recibido).read_bytes() if Path(recibido).exists() else b""
    n = (len(a) + chunk_size - 1) // chunk_size
    malos = sum(1 for i in range(n) if a[i * chunk_size:(i + 1) * chunk_size] != b[i * chunk_size:(i + 1) * chunk_size])
    return {"identico": a == b, "bytes_original": len(a), "bytes_recibido": len(b), "chunks_distintos": malos}


def guardar_json(nombre, datos):
    p = RESULTADOS / nombre
    p.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")
    return p
