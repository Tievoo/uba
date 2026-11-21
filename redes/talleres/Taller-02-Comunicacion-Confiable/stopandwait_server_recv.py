import socket
import random
import argparse
import time
import common

parser = argparse.ArgumentParser()

parser.add_argument("--file", type=str, default="out.bmp", help="Archivo a guardar")
parser.add_argument("--port", type=int, default=12001, help="Puerto en el que escucha")
parser.add_argument("--delay", type=float, default=0.0, help="Simula un delay al enviar frames (tanto de emisor como de receptor)")
parser.add_argument("--loss", type=float, default=0.01, help="Probabilidad de pérdida de un frame")
parser.add_argument("--seed", type=int, default=None, help="Semilla para la simulación de pérdidas")
parser.add_argument("--linger", type=float, default=2.0,
                    help="Segundos que el servidor sigue respondiendo acks después del último frame")

args = parser.parse_args()
out_filename = args.file
random.seed(args.seed)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", args.port))


def receive_and_ack():
    """Recibe un frame, simula pérdidas y responde el ack. Devuelve el frame
    decodificado, o None si se "perdió"."""
    raw_data, addr = sock.recvfrom(common.STOPANDWAIT_DATA_FRAME_SIZE)
    time.sleep(args.delay)
    (is_last, seq_num, data) = common.decode_stopandwait_data_frame(raw_data)

    if random.random() < args.loss:
        print(f"Simulando perdida de frame de datos")
        return None

    ack_frame = common.encode_stopandwait_ack_frame(seq_num)
    if random.random() < args.loss:
        print(f"Simulando perdida de frame de acknowledgement")
    else:
        sock.sendto(ack_frame, addr)
        time.sleep(args.delay)
    return is_last, seq_num, data


expected_seq_num = 0
duplicates = 0
with open(out_filename, "wb") as out:
    while True:
        frame = receive_and_ack()
        if frame is None:
            continue
        (is_last, seq_num, data) = frame

        if seq_num != expected_seq_num:
            # Es una retransmisión de un frame que ya escribimos (el ack
            # anterior se debe haber perdido). Ya le reenviamos el ack;
            # no volvemos a escribir los datos.
            print(f"Frame duplicado (seq_num={seq_num}) -> descartado")
            duplicates += 1
            continue
        expected_seq_num = 1 - expected_seq_num

        out.write(data)
        out.flush()

        if is_last:
            print("ultimo frame -> terminamos")
            break

# Si el ack del último frame se pierde, el emisor lo va a retransmitir. Si
# cerráramos el socket inmediatamente, el emisor quedaría retransmitiendo para
# siempre. Por eso seguimos respondiendo acks hasta que pasen args.linger
# segundos sin recibir nada (idea similar al estado TIME_WAIT de TCP).
sock.settimeout(args.linger)
try:
    while True:
        receive_and_ack()
except (socket.timeout, ConnectionResetError):
    pass

print(f"Descarga guardada en {out_filename} ({duplicates} duplicados descartados)")
sock.close()
