import time
from socket import *  # imports socket module to enable network communication
import numpy as np
import argparse
from TCP import *
option3_error = 0.00
option4_error = 0.00
timeout = 30 / 1000
end_buff = 0

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
            seqnum = i
            data_len = len(chunk)
            chunk = chunk + data_len.to_bytes(2, 'big') + seqnum.to_bytes(2, 'big')

            ch = checksum(chunk)

            sndpkt = chunk + ch
            self.packets.append(sndpkt)  # add packet to array
            if len(chunk) < 1024:  # once a packet is less than 1024 bytes, end of file reached, so break
                image.close()  # close bmp file
                break
            i += 1  # increment loop variable

    def packet_at(self, i):
        return self.packets[i]



def time_out(t):
    if time.time() - t > timeout:
        # print('\t #######  TIME OUT #######' )
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
            self.rcvpkt = self.sockets.recv(4)  # 2 seq, 2  ch thus 7 Bytes
            if np.random.binomial(1, option4_error):
                self.rcvpkt = None
            # print(self.getAck())
        except BlockingIOError as e:
            return False

        if self.rcvpkt:
            return True
        return False

    def corrupt(self):
        ch = checksum(self.rcvpkt[:-2])  # Compute ch on the incoming pkt
        if ch == self.rcvpkt[-2:]:  # Compare ch to the incoming pkt ch
            return False
        return True

    def rdt_send(self, data):
        if np.random.binomial(1, option3_error):
            data = data_pkt_error(data)
        self.sockets.sendto(data, (self.destination, self.port))

    def getAck(self):
        return int.from_bytes(self.rcvpkt[-4:-2], 'big')


def data_pkt_error(pkt: bytes):
    error = int(np.random.randint(0, 255, 1)[0])
    new_pkt = pkt[:error] + error.to_bytes(1, 'big') + pkt[error + 1:]
    return new_pkt

def hand_shake(sock: socket):
    lient_socket.setblocking(False)
    sender = TCP(client_socket)
    packet = Segment()
    packet.flags['S'] = 0b1
    packet.header['seq_num'] = 100
    T = time.time()
    sender.tcp_send(packet.make_packet(''.encode()))
    while not time_out(T):
        incoming = sender.s.recvfrom(1024)
        if incoming:
            break
        print('\rWait', end='')
    if corrupt(incoming):
        if 101 == 101 and 1:  # incoming AckNum, Ack
            packet.header['ack_num'] = 1  # incoming SeqNum + 1
            packet.flags['A'] = 0b1
            sender.tcp_send(packet.make_packet(''.encode()))
            return 1
    return 0


if __name__ == '__main__':
    with socket(AF_INET, SOCK_DGRAM) as client_socket:
        print(hand_shake(client_socket))






"""if False:
    N = args.N
    print(f'**** GB{N} ****')
    image = open('../imgs/select_me.bmp', 'rb')  # opens bitmap file
    p = Packet(image)
    p.make_packet()  # creates all packets to send to server with all headers
    print(len(p.packets))
    end_buff = len(p.packets)
    T = 0
    st_clock = time.time()
    with socket(AF_INET, SOCK_DGRAM) as client_socket:
        client_socket.setblocking(False)
        sender = Sender(12000, gethostname(), client_socket)  # create instance of Sender class
        done = False
        base = 0
        nextseqnum = 0
        rtt_time = 0.30
        dev_rtt = 0
        stamp_time = 0
        while not done:
            print(f'\n\rseq: {nextseqnum}, Base: {base}, \t T: {rtt_time*1000//1}ms, STD: {dev_rtt*1000//1}ms', end='')
            if rtt_time > 0.01:
                timeout = rtt_time + dev_rtt*4

            if nextseqnum < base + N and nextseqnum < end_buff:
                sender.rdt_send(p.packets[nextseqnum])
                stamp_time = time.time()
                if base == nextseqnum:
                    T = time.time()     # Start Timer
                nextseqnum += 1

            if time_out(T):
                T = time.time()        # Reset Timer
                for i in range(base, min(nextseqnum, end_buff)):
                    sender.rdt_send((p.packets[i]))

            if sender.rdt_rcv():
                if not sender.corrupt():
                    rtt = time.time() - stamp_time
                    rtt_time = rtt_time*0.875 + rtt * 0.125
                    dev_rtt = dev_rtt*0.75 + np.abs(rtt - rtt_time)*0.25
                    base = sender.getAck() + 1
                    if base != nextseqnum:
                        T = time.time()   # Reset Timer

            if base == 799:
                done = True

    print(f"\nElapsed time: {time.time() - st_clock}")
"""