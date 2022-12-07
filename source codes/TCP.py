import socket
import time
from socket import *  # imports socket module to enable network communication
import numpy as np
from typing import Tuple

class TCP:
    def __init__(self, SOCKET: socket):
        self.MSS = 1000
        self.s = SOCKET
        self.recv_pkt = None
        self.dst_addr = None
        self.segment = {'source_port': 0,  # 2B
                        'dest_port': 0,  # 2B
                        'seq_num': 0,  # 4B counting bytes of data
                        'ack_num': 0,  # Next expected B
                        'head_len': 0,  # 1B
                        'C': b'0',  # 1 bit congestion
                        'E': b'0',  # 1 bit congestion
                        'U': b'0',  # 1 bit
                        'A': b'0',  # 1 bit Ack
                        'P': b'0',  # 1 bit
                        'R': b'0',  # 1 bit flow
                        'S': b'0',  # 1 bit flow
                        'F': b'0',  # 1 bit flow
                        'rec_window': 0,  # 2B rec window remaining size
                        'checksum': 0,  # 2B
                        }

    def bind(self, HOST, PORT):
        self.s.bind((HOST, PORT))

    def listen(self):
        self.recv_pkt, self.dst_addr = self.s.recvfrom(1024)

    def tcp_recv(self):
        # Check checksum
        # Handle seq
        return self.s.recv(1024)

    def tcp_send(self):
        return self.s.sendto(data, (gethostname(), 12000))

    def accept(self) -> Tuple[socket, tuple]:
        if self.s.connect(self.dst_addr) == 0:
            return self.s, self.dst_addr
        return 0, 0


if __name__ == '__main__':
    with socket(AF_INET, SOCK_DGRAM) as client_socket:
        server = TCP(client_socket)
        server.bind('', 12000)
        server.listen()
        conn, addr = server.accept()
        while True:
            data =  conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
