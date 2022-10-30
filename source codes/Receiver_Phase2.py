import socket
import sys
from socket import *  # imports socket module to enable network communication

states = ['w4zero', 'w4one']
state = states[0]
buffer = b''
once_thru = 0
pkt_len = 1029
ACK = 0xFF


def checksum(data):
    ch = data[0:2]
    for i in range(2, len(data), 2):
        a = int.from_bytes(data[i:i + 2], 'big') + int.from_bytes(ch, 'big')
        if a > 65535:
            a -= 65535
        ch = (~a).to_bytes(3, 'big', signed=True)
        ch = ch[1:]
    return ch


def make_file(path):
    with open(path, 'wb') as image:
        for i, p in enumerate(self.packets):
            skip = i * 1024  # skip variable holds number of bytes already stored
            image.seek(skip)  # skip over bytes already stored as packets
            image.write(p)  # writing packets to file


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
        if self.recv_pkt:
            return True
        return False

    def corrupt(self) -> bool:
        ch = checksum(self.recv_pkt[: -2])  # Compute ch on the incoming pkt
        if ch == self.recv_pkt[-2:]:  # Compare ch to the incoming pkt ch
            return True
        return False

    def has_seqnum(self, seq_num: int) -> bool:
        if int.from_bytes(self.recv_pkt[-3], 'big') == seq_num:
            return True
        return False

    def extract(self):
        pkt_len = int.from_bytes(self.recv_pkt[-5:-3], 'big')
        return self.recv_pkt[:pkt_len]

    def make_pkt(self, ack: int, seq_num: int):
        pkt_len = 1
        pkt_len = pkt_len.to_bytes(2, 'big')
        ack = ack.to_bytes(1, 'big')
        seq_num = seq_num.to_bytes(2, 'big')
        data = ack + pkt_len + seq_num
        return data + checksum(data)

    def udt_send(self, packet):
        self.sockets.sendto(packet, self.dst_addr)


if __name__ == '__main__':
    r = Receiver(12000)

    while True:
        if state == states[0]:
            if r.rdt_rcv(r.rcvpkt) and (r.corrupt(r.rcvpkt) or r.seqnum_one(r.rcvpkt)):
                if oncethru == 1:
                    r.udt_send(r.sndpkt)
            elif r.rdt_rcv(r.rcvpkt) and (not r.corrupt(r.rcvpkt)) and r.seqnum_zero(r.rcvpkt):
                r.extract(r.rcvpkt, r.data)
                r.deliver_data(r.data)
                sndpkt = r.make_pkt(r.ack, 0, r.checksum)
                r.udt_send(sndpkt)
                oncethru = 1
                state = states[1]  # Next State

        elif states == states[1]:
            if r.rdt_rcv(r.rcvpkt) and (r.corrupt(r.rcvpkt) or r.seqnum_zero(r.rcvpkt)):
                r.udt_send(r.sndpkt)
            elif r.rdt_rcv(r.rcvpkt) and (not r.corrupt(r.rcvpkt)) and r.seqnum_one(r.rcvpkt):
                r.extract(r.rcvpkt, r.data)
                r.deliver_data(r.data)
                sndpkt = r.make_pkt(r.ack, 1, r.checksum)
                r.udt_send(sndpkt)
                state = states[0]  # Next State

        r.make_file('../imgs/received_image.bmp')
