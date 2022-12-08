import socket
import time
from socket import *  # imports socket module to enable network communication
import numpy as np
from TCP import *

timeout = 30 / 1000

def time_out(t):
    if time.time() - t > timeout:
        # print('\t #######  TIME OUT #######' )
        return True
    return False

class TCPConnection:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            print('Successful Connection')
        except:
            print('Connection Failed')

    def readlines(self):
        data = self.sock.recv(1024)
        print(data)

class TCP:
    def __init__(self):
        self.MSS = 1000
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

    self.server_port = 20001
    server_addr = (host_ip, self.server_port)  # address of server (IP, Port)

    def checksum(data):
        ch = data[0:2]
        for i in range(2, len(data), 2):
            a = int.from_bytes(data[i:i + 2], 'big') + int.from_bytes(ch, 'big')
            if a > 65535:
                a -= 65535
            ch = (~a).to_bytes(3, 'big', signed=True)
            ch = ch[1:]
        return ch

    def seq_num(self, seq_num: int) -> bool:
        if int.from_bytes(self.recv_pkt[-4:-2], 'big') == seq_num:
            return True
        return False

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

    def tcp_send(self, packet: bytes):
        # Add TCP send protocol

    def rec_window(self):
        # Create receiver window

    def head_len(self):
        # Establish header length

if __name__ == '__main__':

    with socket(AF_INET, SOCK_DGRAM) as server_socket:
        server = TCP(server_socket)
        incoming = server.s.recvfrom(1024)


