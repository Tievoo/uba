import socket
import os
import time
import argparse
import common

parser = argparse.ArgumentParser()

parser.add_argument("--address", type=str, default="127.0.0.1", help="Direccion del servidor")
parser.add_argument("--port", type=int, default=12000, help="Puerto del servidor")
parser.add_argument("--file", type=str, default="tux.bmp", help="Archivo a enviar")
parser.add_argument("--quiet", action="store_true", help="No imprimir cada frame")

args = parser.parse_args()

chunks = common.split_file_in_chunks(args.file)

total = len(chunks)
addr = (args.address, args.port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"enviando {os.path.basename(args.file)} en {total} frames")
start = time.perf_counter()
i = 0
while i < len(chunks):
    if not args.quiet:
        print(i)
    is_last = i == len(chunks) - 1
    data_frame = common.encode_dumb_data_frame(is_last, chunks[i])
    sock.sendto(data_frame, addr)
    i += 1

print(f"transferencia terminada en {time.perf_counter() - start:.4f} s")
sock.close()
