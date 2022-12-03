import socket
import sys
import time
from socket import *  # imports socket module to enable network communication
import numpy as np
import argparse

buffer = b''
once_thru = 0
pkt_len = 1030
ACK = 1
option2_error = 0.00
option5_error = 0.00
expected_seq_num = 0


def checksum(data):
    ch = data[0:2]
    for i in range(2, len(data), 2):
        a = int.from_bytes(data[i:i + 2], 'big') + int.from_bytes(ch, 'big')
        if a > 65535:
            a -= 65535
        ch = (~a).to_bytes(3, 'big', signed=True)
        ch = ch[1:]
    return ch


def make_file(path, data):
    with open(path, 'wb') as image:
        for i, p in enumerate(data):
            skip = i * 1024  # skip variable holds num
            # ber of bytes already stored
            image.seek(skip)  # skip over bytes already stored as packets
            image.write(p)  # writing packets to file


def data_pkt_error(pkt: bytes):
    error = int(np.random.randint(0, 65535, 1)[0])      # Get a random number between 0 ~ 0xFFFF
    new_pkt = error.to_bytes(2, 'big') + pkt[-2:]       # Replace the seqnum by the random number
    return new_pkt


class Receiver:
    def __init__(self, port):
        self.sockets = socket(AF_INET, SOCK_DGRAM)  # Receiver socket
        self.sockets.bind(('', port))  # Receiver socket bind
        self.dst_addr = None
        self.recv_pkt = None

    def __del__(self):
        self.sockets.close()

    def rdt_rcv(self) -> bool:
        self.recv_pkt, self.dst_addr = self.sockets.recvfrom(pkt_len)
        if np.random.binomial(1, option5_error):
            self.recv_pkt = None
        if self.recv_pkt:
            return True
        return False

    def corrupt(self) -> bool:
        ch = checksum(self.recv_pkt[: -2])  # Compute ch on the incoming pkt
        if ch == self.recv_pkt[-2:]:  # Compare ch to the incoming pkt ch
            return False
        print('Faulty checksum ', end='')
        return True

    def has_seqnum(self, seq_num: int) -> bool:
        if int.from_bytes(self.recv_pkt[-4:-2], 'big') == seq_num:
            return True
        return False

    def extract(self):
        pkt_len = int.from_bytes(self.recv_pkt[-6:-4], 'big')
        return self.recv_pkt[:pkt_len]

    def make_pkt(self, seq_num: int):
        seq_num = seq_num.to_bytes(2, 'big')
        return seq_num + checksum(seq_num)

    def udt_send(self, packet: bytes):
        if np.random.binomial(1, option2_error):
            packet = data_pkt_error(packet)
        self.sockets.sendto(packet, self.dst_addr)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-o', type=int, required=True)
    arg_parser.add_argument('-p', type=float, required=False)
    args = arg_parser.parse_args()
    if args.o == 2:
        print(f'Option 2 P={args.p}')
        option2_error = args.p
    elif args.o == 5:
        print(f'Option 5 P={args.p}')
        option5_error = args.p
    elif args.o <= 5:
        option2_error = 0.00
        option5_error = 0.00
    else:
        print(f'Invalid input! {args.o} only option 2&5')

    r = Receiver(12000)
    app_layer_data = []
    extract = None
    sndpkt = None

    while True:
        if r.rdt_rcv():
            if not r.corrupt() and r.has_seqnum(expected_seq_num):
                extract = r.extract()
                app_layer_data.append(extract)
                sndpkt = r.make_pkt(expected_seq_num)
                r.udt_send(sndpkt)
                print(f'\rReceived L= {len(extract)} Ack: {expected_seq_num}', end='')
                expected_seq_num += 1
                if len(extract) < 1024:
                    break
            else:
                r.udt_send(sndpkt)
                print(f'Dual Ack {expected_seq_num}')

    make_file('img.bmp', app_layer_data)
