"""
Receptor sliding window (RWS = 1) con números de secuencia módulo N.
Acepta un frame si su número es (LFR + 1) mod N y responde con ack LFR mod N.
Basado en slidingwindow_server_recv.py del taller.
"""
import socket
import random
import argparse
import common

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, default="out.bmp")
parser.add_argument("--port", type=int, default=12003)
parser.add_argument("--loss", type=float, default=0.0)
parser.add_argument("--seed", type=int, default=None)
parser.add_argument("--linger", type=float, default=1.0)
parser.add_argument("--max-seq", type=int, default=8)
args = parser.parse_args()
N = args.max_seq
random.seed(args.seed)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", args.port))
lfr = -1   # índice absoluto del último frame aceptado (sólo lo conoce el receptor)


def receive_and_ack(out):
    global lfr
    raw_data, addr = sock.recvfrom(common.SLIDINGWINDOW_DATA_FRAME_SIZE)
    (is_last, seq, data) = common.decode_slidingwindow_data_frame(raw_data)
    if random.random() < args.loss:
        return False
    finished = False
    if seq == (lfr + 1) % N:
        out.write(data)
        out.flush()
        lfr += 1
        finished = is_last
    if random.random() >= args.loss:
        sock.sendto(common.encode_slidingwindow_ack_frame(lfr % N), addr)
    return finished


with open(args.file, "wb") as out:
    while not receive_and_ack(out):
        pass
    sock.settimeout(args.linger)
    try:
        while True:
            receive_and_ack(out)
    except (socket.timeout, ConnectionResetError):
        pass
print(f"Descarga guardada en {args.file} ({lfr + 1} frames aceptados)")
sock.close()
