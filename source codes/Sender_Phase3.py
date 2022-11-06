import socket
import time
from socket import *  # imports socket module to enable network communication
import numpy as np
import argparse

option3_error = 0.00
option4_error = 0.00
timeout = 50 / 1000

def checksum(data):
    ch = data[0:2]
    for i in range(2, len(data), 2):
        a = int.from_bytes(data[i:i + 2], 'big') + int.from_bytes(ch, 'big')
        if a > 65535:
            a -= 65535

        ch = (~a).to_bytes(3, 'big', signed=True)
        ch = ch[1:]
    return ch


class Packet:
    def __init__(self, data):
        self.packets = []  # file packet
        self.data = data

    def make_packet(self):
        i = 0  # initialize loop variable
        while True:
            skip = i * 1024  # skip variable holds number of bytes already stored
            self.data.seek(skip)  # skip over bytes already stored as packets
            chunk = self.data.read(1024)  # store 1024 bytes of file as a packet
            seqnum = i % 2
            data_len = len(chunk)
            chunk = chunk + data_len.to_bytes(2, 'big') + seqnum.to_bytes(1, 'big')

            ch = checksum(chunk)

            sndpkt = chunk + ch
            self.packets.append(sndpkt)  # add packet to array
            if len(chunk) < 1024:  # once a packet is less than 1024 bytes, end of file reached, so break
                image.close()  # close bmp file
                break
            i += 1  # increment loop variable


def time_out(t):
    if time.time() - t > timeout:
        print('\t\t\t ############  TIME OUT'*2)
        return True
    return False


class Sender:
    def __init__(self, port: int, destination, sockets: socket):
        self.rcvpkt = None
        self.port = port  # server port number
        self.destination = destination  # server name
        self.sockets = sockets  # client socket
        self.packets = []  # packet array

    def rdt_rcv(self):
        try:
            if not np.random.binomial(1, option4_error):
                self.rcvpkt = self.sockets.recv(6)  # 1 Data, 2 len, 1 seq, 2 ch thus 6 Bytes
        except BlockingIOError as e:
            pass
        if self.rcvpkt:
            return True
        return False

    def corrupt(self):
        ch = checksum(self.rcvpkt[:-2])  # Compute ch on the incoming pkt
        if ch == self.rcvpkt[-2:]:  # Compare ch to the incoming pkt ch
            return False
        print('Faulty checksum ', end='')
        return True

    def rdt_send(self, data):
        if np.random.binomial(1, option3_error):
            data = data_pkt_error(data)
        self.sockets.sendto(data, (self.destination, self.port))

    def isAck(self, seq_num: int):
        if self.rcvpkt[-3] == seq_num:
            if self.rcvpkt[0] == 1:
                print(f'Ack for S{seq_num} ', end='')
                return True
        # print(f'Nack for S{seq_num} ', end='')
        return False


def data_pkt_error(pkt: bytes):
    error = int(np.random.randint(0, 255, 1)[0])
    new_pkt = pkt[:error] + error.to_bytes(1, 'big') + pkt[error + 1:]
    print("## -------ERROR---------  ##", f'Old ch= {checksum(pkt)} New ch= {checksum(new_pkt)}',
          "## -------ERROR--------- ##")
    return new_pkt


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-o', type=int, required=True)
    arg_parser.add_argument('-p', type=float, required=True)
    args = arg_parser.parse_args()
    if args.o == 3:
        print(f'Option 2 P={args.p}')
        option3_error = args.p
    elif args.o == 4:
        print(f'Option 5 P={args.p}')
        option4_error = args.p
    elif args.o == 1:
        option2_error = 0.00
        option5_error = 0.00
    else:
        print(f'Invalid input! {args.o} only option 3&4')

    states = ['w4zero', 'w4Ack0', 'w4one', 'w4Ack1']
    image = open('../imgs/select_me.bmp', 'rb')  # opens bitmap file
    p = Packet(image)
    p.make_packet()  # creates all packets to send to server with all headers
    s = None
    T = 0
    with socket(AF_INET, SOCK_DGRAM) as client_socket:
        client_socket.setblocking(False)
        sender = Sender(12000, gethostname(), client_socket)  # create instance of Sender class

        index = 0
        packet = p.packets[index]
        state = states[0]
        packets_len = len(p.packets)
        while True:
            if state == states[0]:
                sender.rdt_send(packet)
                T = time.time()
                state = states[1]
                print(f'Sent even packet')

            elif state == states[1]:
                if time_out(T):
                    sender.rdt_send(packet)
                    T = time.time()
                    print('Resend Packet')
                if sender.rdt_rcv():
                    if not sender.corrupt() and sender.isAck(0):
                        index += 1
                        if index >= packets_len:
                            break
                        packet = p.packets[index]
                        state = states[2]
                        print(f'Next Packet')

            elif state == states[2]:
                sender.rdt_send(packet)
                T = time.time()
                state = states[3]
                print(f'Sent odd packet')

            elif state == states[3]:
                if time_out(T):
                    sender.rdt_send(packet)
                    T = time.time()
                if sender.rdt_rcv():
                    if not sender.corrupt() and sender.isAck(1):
                        index += 1
                        if index >= packets_len:
                            break
                        packet = p.packets[index]
                        state = states[0]

            if s != state:
                print(state)
                s = state
