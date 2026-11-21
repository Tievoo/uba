import socket
import random
import argparse
import common

parser = argparse.ArgumentParser()

parser.add_argument("--file", type=str, default="out.bmp", help="Archivo a guardar")
parser.add_argument("--port", type=int, default=12000, help="Puerto en el que escucha")
parser.add_argument("--loss", type=float, default=0.01, help="Probabilidad de pérdida de un frame")
parser.add_argument("--seed", type=int, default=None, help="Semilla para la simulación de pérdidas")

args = parser.parse_args()
out_filename = args.file
random.seed(args.seed)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", args.port))
lost = 0
with open(out_filename, "wb") as out:
    while True:
        raw_data, addr = sock.recvfrom(common.DUMB_DATA_FRAME_SIZE)
        (is_last, data) = common.decode_dumb_data_frame(raw_data)

        if random.random() < args.loss:
            print(f"Simulando perdida de frame de datos")
            lost += 1
            # Nota: si el que se pierde es el último frame, el servidor se
            # queda esperando para siempre (el protocolo no tiene forma de
            # recuperarse)
            continue

        out.write(data)
        out.flush()

        if is_last:
            print("ultimo frame -> terminamos")
            break

print(f"Descarga guardada en {out_filename} ({lost} frames perdidos)")
sock.close()
