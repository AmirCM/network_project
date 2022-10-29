import socket
import sys
from socket import *  # imports socket module to enable network communication


ack = True
states = ['w4zero', 'w4one']
state = states[0]
buffer = b''
seqNum = False
once_thru = 0


class Receiver:
    def __init__(self, port, sockets):
            self.port = port  # Receiver port number
            self.sockets = sockets  # Receiver socket
            self.packets = []  # Receiver packets
            self.socket_bind()  # Receiver bind to socket


    def rdt_rcv(packet):# Function to receive packets from sender
        if not packet:
            return False
        else:
            return True

    def checksum(data):# Function to generate checksum
        ch = data[0:2]
        for i in range(2, len(data), 2):
            a = int.from_bytes(data[i:i + 2], 'big') + int.from_bytes(ch, 'big')
            if a > 65535:
                a -= 65535
            ch = (~a).to_bytes(3, 'big', signed=True)
            ch = ch[1:]
        return ch


    def corrupt(rcv_pkt):# Function to check for corruption
        pkt_len = len(rcv_pkt)
        if r.checksum(rcv_pkt[0:(pkt_len - 1)]) == rcv_pkt[(pkt_len - 1):pkt_len]:
            return False
        else:
            return True

    def get_seq(rcv_pkt):# Function to extract sequence number from received packet
        if rcv_pkt[0:1] == '1':
            return True
        if rcv_pkt[0:1] == '0':
            return False

    def extract(packet):# Function to extract data from received packet
        received_packet_length = len(packet)
        return packet[0:(received_packet_length - 5)]

    def deliver_data(data):# Function to deliver data
        global buffer
        buffer = buffer + data
        return

    def make_pkt(seqNum, ack, checksum):# Function to make packet that will be delivered to sender
        packet = str(int(seqNum)).encode + ack + checksum
        return packet

    def udt_send(packet): # Function to send packet to sender
        sender_socket = socket(AF_INET, SOCK_DGRAM)
        sender_socket.sendto(packet, (sender.destination, sender.port))
        sender_socket.close()
        return

    def start(self): # Function to start
        self.packets = []
        while True:
            incoming, address = self.sockets.recvfrom(1024)
            self.packets.append(incoming)  # packet to array
            if len(incoming) < 1024:
                break

    def socket_bind(self): # Function to bind socket
            self.sockets.bind(('', self.port))  # binds to the socket

if __name__ == '__main__': # Main function begins here
        r = Receiver(12000, socket(AF_INET, SOCK_DGRAM))
        r.start()
        recv_pkt = r.sockets.recvfrom(1024)
        data = r.extract(recv_pkt)

        if state == states[0]: # Conditional statement for first state

            if r.rdt_rcv(recv_pkt) and (r.corrupt(recv_pkt) or r.get_seq(recv_pkt) == 1):
                if once_thru == 1:
                    checksum = r.checksum(seqNum, data)
                    send_pkt = r.make_pkt(1, ack, checksum)
                    r.udt_send(send_pkt)

            elif r.rdt_rcv(recv_pkt) and (not r.corrupt(recv_pkt)) and r.get_seq(recv_pkt) == 0:
                r.extract(recv_pkt, data)
                r.deliver_data(data)
                checksum = r.checksum(seqNum, data)
                send_pkt = r.make_pkt(0, ack, checksum)
                r.udt_send(send_pkt)
                once_thru = 1
                state = states[1]  # Next State

        elif states == states[1]: # Conditional statement for second state

            if r.rdt_rcv(recv_pkt) and (r.corrupt(recv_pkt) or r.get_seq(recv_pkt) == 0):
                checksum = r.checksum(seqNum, data)
                send_pkt = r.make_pkt(0, ack, checksum)
                r.udt_send(send_pkt)

            elif r.rdt_rcv(recv_pkt) and (not r.corrupt(recv_pkt)) and r.get_seq(recv_pkt) == 1:
                r.extract(recv_pkt)
                r.deliver_data(data)
                checksum = r.checksum(seqNum, data)
                send_pkt = r.make_pkt(1, ack, checksum)
                r.udt_send(send_pkt)
                state = states[0]  # Next State
