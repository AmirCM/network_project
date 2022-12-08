import socket
import time
from socket import *  # imports socket module to enable network communication
import numpy as np
from typing import Tuple


def checksum(data):
    ch = data[0:2]
    for i in range(2, len(data), 2):
        a = int.from_bytes(data[i:i + 2], 'big') + int.from_bytes(ch, 'big')
        if a > 65535:
            a -= 65535

        ch = (~a).to_bytes(3, 'big', signed=True)
        ch = ch[1:]
    return ch


class Segment:
    def __init__(self):
        self.header_map = [4, 1, 1, 0, 2, 2]
        self.header = {
                       'seq_num': 0,  # 4B counting bytes of data
                       'ack_num': 0,  # Next expected 4B
                       'head_len': 0,  # 1B
                       'empty': 0,  # 1B
                       'rec_window': 0,  # 2B rec window remaining size
                       'checksum': 0,  # 2B
                       }
        self.flags = {'C': 0b0,  # 1 bit congestion
                      'E': 0b0,  # 1 bit congestion
                      'U': 0b0,  # 1 bit
                      'A': 0b0,  # 1 bit Ack
                      'P': 0b0,  # 1 bit
                      'R': 0b0,  # 1 bit flow
                      'S': 0b0,  # 1 bit flow
                      'F': 0b0,  # 1 bit flow
                      }
        self.data = None
        
    def reset_flags(self): 
         self.flags = {'C': 0b0,  # 1 bit congestion
                      'E': 0b0,  # 1 bit congestion
                      'U': 0b0,  # 1 bit
                      'A': 0b0,  # 1 bit Ack
                      'P': 0b0,  # 1 bit
                      'R': 0b0,  # 1 bit flow
                      'S': 0b0,  # 1 bit flow
                      'F': 0b0,  # 1 bit flow
                      }

    def make_packet(self, data):
        for i, h in enumerate(self.header.values()):
            if self.header_map[i] != 0:
                if i == 0:
                    chunck = h.to_bytes(self.header_map[i], 'big')
                else:
                    chunck += h.to_bytes(self.header_map[i], 'big')
            else:
                h = 0b0
                for f in self.flags.values():
                    h = h<<1 | f
                chunck += h.to_bytes(1, 'big')

        ch = checksum(chunck + data)
        return chunck + ch + data

class TCP:
    def __init__(self, SOCKET: socket):
        self.MSS = 1000
        self.s = SOCKET
        self.recv_pkt = None
        self.dst_addr = None
        self.segment = Segment()

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
    s = Segment()
    print(s.make_packet('HI'.encode()))
    """with socket(AF_INET, SOCK_DGRAM) as client_socket:
        server = TCP(client_socket)
        server.bind('', 12000)
        server.listen()
        conn, addr = server.accept()
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)"""
