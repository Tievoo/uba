"""
Receptor del protocolo sliding window con ventana de recepción de tamaño 1
(RWS = 1, es decir, Go-Back-N del lado del receptor).

Variables (nomenclatura de Peterson & Davie, sección 2.5):
- LFR (last frame received): último frame recibido en orden y escrito en disco.
  El próximo frame aceptable es LFR + 1 (la ventana tiene un único lugar).

Para cada frame recibido:
- Si su número de secuencia es LFR + 1, se escribe y se avanza LFR.
- Si no (frame duplicado o que llegó fuera de orden), se descarta.
- En ambos casos se responde un ack *acumulativo* con LFR: "recibí todo hasta
  LFR inclusive". El emisor hace last_ack_recvd = max(last_ack_recvd, ack), así
  que un ack viejo o repetido no le hace daño.
"""
import socket
import random
import argparse
import common

parser = argparse.ArgumentParser()

parser.add_argument("--file", type=str, default="out.bmp", help="Archivo a guardar")
parser.add_argument("--port", type=int, default=12002, help="Puerto en el que escucha")
parser.add_argument("--loss", type=float, default=0.01, help="Probabilidad de pérdida de un frame")
parser.add_argument("--seed", type=int, default=None, help="Semilla para la simulación de pérdidas")
parser.add_argument("--linger", type=float, default=2.0,
                    help="Segundos que el servidor sigue respondiendo acks después del último frame")

args = parser.parse_args()
out_filename = args.file
random.seed(args.seed)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", args.port))

last_frame_received = -1   # LFR
stats = {"aceptados": 0, "descartados": 0, "perdidos": 0}


def receive_and_ack(out):
    """Recibe un frame, lo escribe si es el esperado y responde el ack
    acumulativo. Devuelve True si se escribió el último frame del fichero."""
    global last_frame_received
    raw_data, addr = sock.recvfrom(common.SLIDINGWINDOW_DATA_FRAME_SIZE)
    (is_last, sequence_number, data) = common.decode_slidingwindow_data_frame(raw_data)

    if random.random() < args.loss:
        print(f"Simulando perdida de frame de datos")
        stats["perdidos"] += 1
        return False

    finished = False
    if sequence_number == last_frame_received + 1:
        out.write(data)
        out.flush()
        last_frame_received = sequence_number
        stats["aceptados"] += 1
        finished = is_last
    else:
        # Duplicado (sequence_number <= LFR) o fuera de orden (> LFR + 1):
        # con RWS = 1 no lo podemos guardar, lo descartamos
        stats["descartados"] += 1

    ack_frame = common.encode_slidingwindow_ack_frame(last_frame_received)
    if random.random() < args.loss:
        print(f"Simulando perdida de frame de acknowledgement")
    else:
        sock.sendto(ack_frame, addr)
    return finished


with open(out_filename, "wb") as out:
    while not receive_and_ack(out):
        pass
    print("ultimo frame -> terminamos")

    # Igual que en stop and wait: seguimos respondiendo acks un rato por si el
    # ack del último frame (o de alguno anterior) se perdió
    sock.settimeout(args.linger)
    try:
        while True:
            receive_and_ack(out)
    except (socket.timeout, ConnectionResetError):
        pass

print(f"Descarga guardada en {out_filename} {stats}")
sock.close()
