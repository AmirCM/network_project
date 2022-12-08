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


def corrupt(pkt: bytes) -> bool:
    ch = checksum(pkt[13:15])  # Compute ch on the incoming pkt
    if ch == pkt[13:15]:  # Compare ch to the incoming pkt ch
        return False
    return True

def get_seqNum(pkt: bytes) -> bool:
    return int.from_bytes(pkt[0:4], 'big')

def get_ack_num(pkt: bytes) -> bool:
    return int.from_bytes(pkt[4:7], 'big')

def get_head_len(pkt: bytes) -> bool:
    return int.from_bytes(pkt[8], 'big')

def get_rec_window(pkt: bytes) -> bool:
    return int.from_bytes(pkt[11:13], 'big')

def get_checksum(pkt: bytes) -> bool:
    return int.from_bytes(pkt[13:15], 'big')


def check_flag_c(pkt: bytes):
    if int.from_bytes(pkt[10], 'big'):
        return True
    else:
        return False


def check_flag_ack(pkt: bytes):
    if int.from_bytes(pkt[10], 'big'):
        return True
    else:
        return False


def check_flag_e(pkt: bytes):
    if int.from_bytes(pkt[10], 'big'):
        return True
    else:
        return False


def check_flag_r(pkt: bytes):
    if int.from_bytes(pkt[10], 'big'):
        return True
    else:
        return False


def check_flag_sync(pkt: bytes):
    if int.from_bytes(pkt[10], 'big'):
        return True
    else:
        return False


def check_flag_f(pkt: bytes):
    if int.from_bytes(pkt[10], 'big'):
        return True
    else:
        return False

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
            
    def set_seqNum(seq_num: int):
        pass

    def set_ack_num(ack_num: int):
        pass

    def set_head_len(head_len: int):
        pass

    def set_rec_window(rec_window: int):
        pass

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
        while True:
            incoming, address = self.s.recvfrom(1024)
            if not corrupt(incoming):
                break
        if check_flag_sync(incoming):
            seq_num = get_seqNum(incoming)
            packet = Segment()
            packet.header['ack_num'] = seq_num + 1
            packet.header['seq_num'] = 10
            packet.flags['A'] = 0b1
            packet.flags['S'] = 0b1
            self.tcp_send(packet.make_packet(''.encode()))
            incoming, address = self.s.recvfrom(1024)

    def tcp_recv(self, l):
        # Check checksum
        # Handle seq
        return self.s.recv(l)

    def tcp_send(self, pkt):
        return self.s.sendto(pkt, (gethostname(), 12000))

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
