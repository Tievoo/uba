import socket
import os
import argparse
import common

parser = argparse.ArgumentParser()

parser.add_argument("--address", type=str, default="127.0.0.1", help="Direccion del servidor")
parser.add_argument("--file", type=str, default="tux.bmp", help="Archivo a enviar")
parser.add_argument("--timeout", type=float, default=0.5, help="Timeout en segundos")

args = parser.parse_args()

chunks = common.split_file_in_chunks(args.file)

total = len(chunks)
addr = (args.address, 12001)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(args.timeout)

print(f"enviando {os.path.basename(args.file)} en {total} frames")
i = 0
seq_num = 0
while i < len(chunks):
    is_last = i == len(chunks) - 1
    data_frame = common.encode_stopandwait_data_frame(is_last, seq_num, chunks[i])
    sock.sendto(data_frame, addr)
    try:
        raw_data = sock.recv(common.STOPANDWAIT_ACK_FRAME_SIZE)
    except socket.timeout:
        print(f'timeout para frame {i}')
        continue
    ack_seq_num = common.decode_stopandwait_ack_frame(raw_data)
    if ack_seq_num != seq_num:
        # Ack de un frame viejo (por ejemplo, llegó tarde): lo ignoramos y
        # seguimos esperando el ack del frame actual
        continue
    seq_num = 1 - seq_num
    i += 1

print("transferencia terminada")
sock.close()

