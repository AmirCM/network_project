import socket
import time
from socket import *  # imports socket module to enable network communication
import numpy as np
from TCP import *


def make_file(path, data):
    with open(path, 'wb') as image:
        for i, p in enumerate(data):
            skip = i * 1000  # skip variable holds num
            # ber of bytes already stored
            image.seek(skip)  # skip over bytes already stored as packets
            image.write(p)  # writing packets to file


class Receiver:
    def __init__(self, port):
        self.sockets = socket(AF_INET, SOCK_DGRAM)  # Receiver socket
        self.dst_addr = None
        self.recv_pkt = None
        self.port = port

    def rdt_rcv(self) -> bool:
        self.recv_pkt, self.dst_addr = self.sockets.recvfrom(1024)
        if not corrupt(self.recv_pkt) and self.recv_pkt:
            return True
        return False

    def extract(self):
        pkt_len = get_head_len(self.recv_pkt)
        return self.recv_pkt[pkt_len:]

    def listen(self):
        while True:
            incoming, dst_addr = self.sockets.recvfrom(1024)
            if not corrupt(incoming):
                break
        if check_flag_sync(incoming):
            seq_num = get_seqNum(incoming)
            packet = Segment()
            packet.header['ack_num'] = seq_num + 1
            packet.header['seq_num'] = 10
            packet.flags['A'] = 0b1
            packet.flags['S'] = 0b1
            pkt = packet.make_packet(''.encode())
            self.sockets.sendto(pkt, dst_addr)
        else:
            return False

        while True:
            incoming, dst_addr = self.sockets.recvfrom(1024)
            if not corrupt(incoming):
                break
        if check_flag_ack(incoming) and get_ackNum(incoming) == 11:
            print('Connection successful')
            self.sockets.connect(dst_addr)
            return True


if __name__ == '__main__':
    r = Receiver(12000)
    r.sockets.bind(('', 12000))
    window = ['' for _ in range(819)]
    if r.listen():

        seg = Segment()
        while True:

            if r.rdt_rcv():
                seqNum = get_seqNum(r.recv_pkt) // 1000
                data = r.extract()
                print(len(data))
                if not window[seqNum]:
                    seg.reset_flags()
                    window[seqNum] = data
                    seg.set_ackNum((seqNum + 1) * 1000)
                    seg.flags['A'] = 0b1
                    r.sockets.send(seg.make_packet(''.encode()))
                    if seqNum == 818:
                        break

            else:
                r.sockets.send(seg.make_packet(''.encode()))

    make_file('img.bmp', window)
