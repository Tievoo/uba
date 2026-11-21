"""
Emisor sliding window con espacio de números de secuencia FINITO: en el frame
viaja `índice mod N` (N = --max-seq) en vez del índice del chunk.

Internamente el emisor lleva índices absolutos (LAR, LFS). Cuando llega un ack
con número `a` (mod N), lo traduce al índice absoluto k más cercano por encima
de LAR:  k = LAR + ((a - LAR) mod N),  o sea k en [LAR, LAR + N - 1].
Esa traducción es inequívoca sólo si la ventana tiene a lo sumo N - 1 frames
sin ack (SWS <= N - 1), que es justamente la condición que queremos probar.

Basado en slidingwindow_client_send.py del taller.
"""
import socket
import os
import time
import argparse
import collections
import common

parser = argparse.ArgumentParser()
parser.add_argument("--address", type=str, default="127.0.0.1")
parser.add_argument("--port", type=int, default=12003)
parser.add_argument("--file", type=str, default="tux.bmp")
parser.add_argument("--timeout", type=float, default=0.5)
parser.add_argument("--window-size", type=int, default=7)
parser.add_argument("--max-seq", type=int, default=8, help="N: cantidad de números de secuencia distintos")
args = parser.parse_args()
N = args.max_seq

chunks = common.split_file_in_chunks(args.file)
total = len(chunks)
last_chunk = total - 1
addr = (args.address, args.port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(args.timeout)
print(f"enviando {os.path.basename(args.file)} en {total} frames, SWS={args.window_size}, N={N}")

last_ack_recvd = -1
last_frame_sent = -1
sent = 0
Timer = collections.namedtuple('Timer', ['when', 'index'])
timers = []


def send_chunk_and_add_timer(i):
    global sent
    frame = common.encode_slidingwindow_data_frame(i == last_chunk, i % N, chunks[i])
    sock.sendto(frame, addr)
    sent += 1
    timers.append(Timer(when=time.time() + args.timeout, index=i))


start = time.perf_counter()
while last_ack_recvd != last_chunk:
    while timers and timers[0].when <= time.time():
        (_, i) = timers.pop(0)
        if i <= last_ack_recvd:
            continue
        send_chunk_and_add_timer(i)

    while last_frame_sent - last_ack_recvd < args.window_size and last_frame_sent != last_chunk:
        last_frame_sent += 1
        send_chunk_and_add_timer(last_frame_sent)

    try:
        raw_data = sock.recv(common.SLIDINGWINDOW_ACK_FRAME_SIZE)
        (a,) = common.decode_slidingwindow_ack_frame(raw_data)
        k = last_ack_recvd + ((a - last_ack_recvd) % N)
        if k <= last_frame_sent:
            last_ack_recvd = max(last_ack_recvd, k)
    except (socket.timeout, ConnectionResetError):
        pass

elapsed = time.perf_counter() - start
print(f"transferencia terminada en {elapsed:.4f} s ({sent} frames enviados, {sent - total} retransmisiones)")
sock.close()
