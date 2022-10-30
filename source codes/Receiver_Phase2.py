import socket
import sys
from socket import *  # imports socket module to enable network communication

states = ['w4zero', 'w4one']
state = states[0]
buffer = b''
once_thru = 0
pkt_len = 1029


def checksum(data):
    ch = data[0:2]
    for i in range(2, len(data), 2):
        a = int.from_bytes(data[i:i + 2], 'big') + int.from_bytes(ch, 'big')
        if a > 65535:
            a -= 65535
        ch = (~a).to_bytes(3, 'big', signed=True)
        ch = ch[1:]
    return ch


class Receiver:
    def __init__(self, port):

        self.sockets = socket(AF_INET, SOCK_DGRAM)  # Receiver socket
        self.sockets.bind(('', port))  # Receiver socket bind

        self.dst_addr = None
        self.packets = []  # Receiver packets
        self.recv_pkt = []
        self.data = None
        self.ACK = None
        self.checksum = None
        self.seqNum = None

    def __del__(self):
        self.sockets.close()

    def rdt_rcv(self):
        self.recv_pkt, self.dst_addr = self.sockets.recvfrom(pkt_len)
        if self.recv_pkt:
            return True
        return False

    def corrupt(self):
        ch = checksum(self.recv_pkt[: -2])      # Compute ch on the incoming pkt
        if ch == self.recv_pkt[-2:]:            # Compare ch to the incoming pkt ch
            return True
        return False

    def has_seqnum(self, seq_num):
        if int.from_bytes(self.recv_pkt[-3], 'big') == seq_num:
            return True
        return False


    def extract(self, recv_pkt, data):
        received_packet_length = len(recv_pkt)
        return recv_pkt[0:(received_packet_length - 5)]

    def deliver_data(self, data):
        global buffer
        buffer = buffer + data
        return

    def make_pkt(self, ack, seqNum, checksum):
        packet = str(int(seqNum)).encode + ack + checksum
        return packet

    def make_file(self, path):
        with open(path, 'wb') as image:
            for i, p in enumerate(self.packets):
                skip = i * 1024  # skip variable holds number of bytes already stored
                image.seek(skip)  # skip over bytes already stored as packets
                image.write(p)  # writing packets to file

    def udt_send(self, packet):
        sender_socket = socket(AF_INET, SOCK_DGRAM)
        sender_socket.sendto(packet, (r.destination, r.port))
        sender_socket.close()
        return

    def start(self):
        self.packets = []
        while True:
            incoming, address = self.sockets.recvfrom(pkt_len)
            self.packets.append(incoming)  # packet to array
            if len(incoming) < 1027:
                break


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
