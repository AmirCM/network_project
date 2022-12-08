import socket
import time
from socket import *  # imports socket module to enable network communication
import numpy as np
from TCP import *


class Receiver:
    def __init__(self, port):
        self.sockets = socket(AF_INET, SOCK_DGRAM)  # Receiver socket
        self.dst_addr = None
        self.recv_pkt = None
        self.port = port

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
        # print('Faulty checksum ', end='')
        return True

    def extract(self):
        pkt_len = int.from_bytes(self.recv_pkt[-6:-4], 'big')
        return self.recv_pkt[:pkt_len]

    def make_pkt(self, seq_num: int):
        seq_num = seq_num.to_bytes(2, 'big')
        return seq_num + checksum(seq_num)

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
            incoming, dst_addr = sockets.recvfrom(1024)
            if not corrupt(incoming):
                break
        if check_flag_ack(incoming) and get_ack_num(incoming) == 11:
            print('Connection successful')
            return True


if __name__ == '__main__':
        r = Receiver(12000)
        r.sockets.bind(('', 12000))
        r.listen()
