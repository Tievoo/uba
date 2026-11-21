"""
Emulador de canal: proxy UDP que se ubica entre cliente y servidor y simula
las propiedades de un enlace real (similar a lo que hace `tc netem` en Linux).

    cliente  --->  [canal :listen-port]  --->  servidor :server-port
    cliente  <---  [canal              ]  <---  servidor

Para cada datagrama, en cada dirección:
  - pérdida aleatoria (--loss) o en ráfagas (--burst-prob / --burst-len)
  - tiempo de transmisión según la tasa del enlace (--rate, en bits/s):
    los frames se encolan y salen de a uno (como en un enlace serie)
  - retardo de propagación (--delay) con jitter opcional
  - con probabilidad --late-prob, un retardo extra --late-delay. Esto hace que
    el frame llegue *después* de frames enviados más tarde (reordenamiento),
    como si hubiera tomado otro camino o se hubiera quedado en una cola.

El canal termina solo luego de --idle-exit segundos sin tráfico e imprime
estadísticas en JSON en la última línea de su salida.
"""
import argparse
import heapq
import itertools
import json
import random
import select
import socket
import time

parser = argparse.ArgumentParser()
parser.add_argument("--listen-port", type=int, default=13000)
parser.add_argument("--server-address", type=str, default="127.0.0.1")
parser.add_argument("--server-port", type=int, required=True)
parser.add_argument("--delay", type=float, default=0.0, help="Retardo de propagación en un sentido (s)")
parser.add_argument("--jitter", type=float, default=0.0, help="Jitter uniforme +- (s)")
parser.add_argument("--rate", type=float, default=0.0, help="Tasa del enlace en bits/s (0 = infinita)")
parser.add_argument("--loss", type=float, default=0.0, help="Probabilidad de pérdida por frame")
parser.add_argument("--burst-prob", type=float, default=0.0, help="Probabilidad de iniciar una ráfaga de pérdidas")
parser.add_argument("--burst-len", type=int, default=0, help="Frames perdidos por ráfaga")
parser.add_argument("--late-prob", type=float, default=0.0, help="Probabilidad de que un frame se demore de más")
parser.add_argument("--late-delay", type=float, default=0.0, help="Retardo extra para los frames demorados (s)")
parser.add_argument("--dirs", choices=["both", "fwd", "rev"], default="both",
                    help="Direcciones a las que se aplican pérdidas y demoras extra "
                         "(fwd = datos cliente->servidor, rev = acks servidor->cliente)")
parser.add_argument("--seed", type=int, default=None)
parser.add_argument("--idle-exit", type=float, default=3.0)
args = parser.parse_args()

rng = random.Random(args.seed)

sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_client.bind(("127.0.0.1", args.listen_port))
sock_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_server.bind(("127.0.0.1", 0))
for s in (sock_client, sock_server):
    s.setblocking(False)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1 << 20)

server_addr = (args.server_address, args.server_port)
client_addr = None


class Direction:
    def __init__(self, name, impaired):
        self.name = name
        self.impaired = impaired
        self.next_free = 0.0      # momento en que el enlace queda libre
        self.burst_left = 0
        self.stats = {"recibidos": 0, "perdidos": 0, "demorados": 0}


fwd = Direction("fwd", args.dirs in ("both", "fwd"))
rev = Direction("rev", args.dirs in ("both", "rev"))

queue = []                # heap de (momento_de_entrega, n, socket, datos, destino)
counter = itertools.count()


def enqueue(direction, data, out_sock, dest):
    direction.stats["recibidos"] += 1
    if direction.impaired:
        if direction.burst_left > 0:
            direction.burst_left -= 1
            direction.stats["perdidos"] += 1
            return
        if args.burst_len > 0 and rng.random() < args.burst_prob:
            direction.burst_left = args.burst_len - 1
            direction.stats["perdidos"] += 1
            return
        if rng.random() < args.loss:
            direction.stats["perdidos"] += 1
            return

    now = time.perf_counter()
    if args.rate > 0:
        # El frame espera a que el enlace se libere y tarda len*8/rate en salir
        departure = max(now, direction.next_free) + len(data) * 8 / args.rate
        direction.next_free = departure
    else:
        departure = now
    arrival = departure + args.delay
    if args.jitter > 0:
        arrival += rng.uniform(-args.jitter, args.jitter)
        arrival = max(arrival, departure)
    if direction.impaired and rng.random() < args.late_prob:
        arrival += args.late_delay
        direction.stats["demorados"] += 1
    heapq.heappush(queue, (arrival, next(counter), out_sock, data, dest))


last_activity = time.perf_counter()
started = False
while True:
    now = time.perf_counter()

    # Entrego los frames cuyo momento de llegada ya pasó
    while queue and queue[0][0] <= now:
        (_, _, out_sock, data, dest) = heapq.heappop(queue)
        try:
            out_sock.sendto(data, dest)
        except OSError:
            pass
        last_activity = now

    readable, _, _ = select.select([sock_client, sock_server], [], [], 0)
    for s in readable:
        while True:
            try:
                data, addr = s.recvfrom(65535)
            except (BlockingIOError, ConnectionResetError):
                break
            started = True
            last_activity = time.perf_counter()
            if s is sock_client:
                client_addr = addr
                enqueue(fwd, data, sock_server, server_addr)
            elif client_addr is not None:
                enqueue(rev, data, sock_client, client_addr)

    if started and not queue and time.perf_counter() - last_activity > args.idle_exit:
        break

    if not readable:
        # Espera corta (en Python >= 3.11, time.sleep en Windows tiene
        # resolución sub-milisegundo)
        wait = 0.0005
        if queue:
            wait = min(wait, max(0.0, queue[0][0] - time.perf_counter()))
        time.sleep(wait)

print(json.dumps({"fwd": fwd.stats, "rev": rev.stats}), flush=True)
