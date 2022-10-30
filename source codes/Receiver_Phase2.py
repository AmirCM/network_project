import socket
import sys
from socket import *  # imports socket module to enable network communication


states = ['w4zero', 'w4one']
state = states[0]
buffer = b''
once_thru = 0


class Receiver:
    def __init__(self, port, sockets, destination, data, ack, checksum, seqNum):
        self.port = port  # Receiver port number
        self.destination = destination
        self.sockets = sockets  # Receiver socket
        self.packets = []  # Receiver packets
        self.socket_bind()  # Receiver bind to socket
        self.recv_pkt = []
        self.data = data
        self.ACK = ack
        self.checksum = checksum
        self.seqNum = seqNum

    def rdt_rcv(self):
        self.recv_pkt, client_address = self.sockets.recvfrom(4)
        if self.recv_pkt:
            True
        else:
            False

    def checksum(self, data):
        ch = data[0:2]
        for i in range(2, len(data), 2):
            a = int.from_bytes(data[i:i + 2], 'big') + int.from_bytes(ch, 'big')
            if a > 65535:
                a -= 65535
            ch = (~a).to_bytes(3, 'big', signed=True)
            ch = ch[1:]
        return ch

    def corrupt(self, recv_pkt):
        ch = self.checksum(recv_pkt[0:(len(recv_pkt) - 2)])
        if ch == recv_pkt[len(recv_pkt - 2):]:
            True
        else:
            False

    def seqnum_zero(self, recv_pkt):
        if recv_pkt[0] == 0:
            return True
        else:
            return False

    def seqnum_one(self, recv_pkt):
        if recv_pkt[0] == 1:
            return True
        else:
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
            incoming, address = self.sockets.recvfrom(1027)
            self.packets.append(incoming)  # packet to array
            if len(incoming) < 1027:
                break

    def socket_bind(self):
        self.sockets.bind(('', self.port))


if __name__ == '__main__':
    r = Receiver(12000, socket(AF_INET, SOCK_DGRAM))
    r.start()

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
