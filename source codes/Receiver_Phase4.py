import socket
import sys
from socket import *  # imports socket module to enable network communication
import numpy as np
import argparse

buffer = b''
once_thru = 0
pkt_len = 1029
ACK = 1
option2_error = 0.00
option5_error = 0.00
expected_seq_num = 1


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


def make_noise_pkt(ack: int, seq_num: int):
    pkt_len = 1
    pkt_len = pkt_len.to_bytes(2, 'big')
    ack = ack.to_bytes(1, 'big')
    seq_num = seq_num.to_bytes(2, 'big')
    data = ack + pkt_len + seq_num
    ch = checksum(data)
    ack = 0
    ack = ack.to_bytes(2, 'big')
    return ack + pkt_len + seq_num + ch


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
        if self.recv_pkt[-3] == seq_num:
            # print(f'Seq: {seq_num}')
            return True
        return False

    def extract(self):
        pkt_len = int.from_bytes(self.recv_pkt[-5:-3], 'big')
        return self.recv_pkt[:pkt_len]

    def make_pkt(self, ack: int, seq_num: int):
        pkt_len = 1
        pkt_len = pkt_len.to_bytes(2, 'big')
        ack = ack.to_bytes(2, 'big')
        seq_num = seq_num.to_bytes(2, 'big')
        data = ack + pkt_len + seq_num
        return data + checksum(data)

    def udt_send(self, packet):
        self.sockets.sendto(packet, self.dst_addr)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-o', type=int, required=True)
    arg_parser.add_argument('-p', type=float, required=True)
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
    List = []
    extract = None
    sndpkt = None
    once_thru = 0
    s = None

    while True:
        if r.rdt_rcv():
            if not r.corrupt() and r.has_seqnum(expected_seq_num):
                extract = r.extract()
                print(f'Received L= {len(extract)} ', end='')
                List.append(extract)

                sndpkt = r.make_pkt(ACK, expected_seq_num)
                if np.random.binomial(1, option2_error):
                    noise_sndpkt = make_noise_pkt(ACK, 1)
                    r.udt_send(noise_sndpkt)
                    print('Noise', end='')
                else:
                    r.udt_send(sndpkt)
                    expected_seq_num += 1

                once_thru = 1

                print(f'Sent ACK {len(sndpkt)} S0')
                if len(extract) < 1024:
                    break
        else:
            r.udt_send(sndpkt)
            print(f'Sent ACK {len(sndpkt)} S1')

            if len(extract) < 1024:
                break

    make_file('img.bmp', List)
