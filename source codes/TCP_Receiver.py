import socket
import time
from socket import *  # imports socket module to enable network communication
import numpy as np
from TCP import *

class Receiver:

    def __init__(self, port):
        self.sockets = socket(AF_INET, SOCK_DGRAM)  # Receiver socket
        self.sockets.bind(('', port))  # Receiver socket bind
        self.dst_addr = None
        self.recv_pkt = None

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


if __name__ == '__main__':
    with socket(AF_INET, SOCK_DGRAM) as server_socket:
        server = TCP(server_socket)
        server.bind('', 12000)
        if server.listen():
            print('Handshake complete')










