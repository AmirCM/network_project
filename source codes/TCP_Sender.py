import time
from socket import *  # imports socket module to enable network communication
import numpy as np
import argparse
from TCP import *

option3_error = 0.00
option4_error = 0.00
timeout = 30 / 1000
end_buff = 818000


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
            skip = i * 1000  # skip variable holds number of bytes already stored
            self.data.seek(skip)  # skip over bytes already stored as packets
            chunk = self.data.read(1000)  # store 1024 bytes of file as a packet
            self.packets.append(chunk)  # add Segment to array

            if len(chunk) < 1000:  # once a packet is less than 1024 bytes, end of file reached, so break
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
            self.rcvpkt = self.sockets.recv(20)  # 2 seq, 2  ch thus 7 Bytes
            if corrupt(self.rcvpkt):
                return False
            if np.random.binomial(1, option4_error):
                self.rcvpkt = None
        except BlockingIOError as e:
            return False

        if self.rcvpkt:
            return True
        return False

    def rdt_send(self, data):
        # self.sockets.sendto(data, (self.destination, self.port))
        self.sockets.send(data)

    def close(self):
        seg = Segment()
        seg.flags['F'] = 0b1
        self.sockets.send(seg.make_packet(''.encode()))
        timeout = 0.5
        T = time.time()
        while True:
            if time_out(T):
                break
            if self.rdt_rcv():
                if check_flag_f(self.rcvpkt):
                    break

    def handShake(self):
        x = 100
        seg = Segment()

        seg.flags['S'] = 0b1
        seg.set_seqNum(x)

        T = time.time()
        sdt_pkt = seg.make_packet(''.encode())
        print(sdt_pkt)
        self.sockets.sendto(sdt_pkt, (self.destination, self.port))
        incoming = 0
        while not time_out(T):
            try:
                incoming, addr = self.sockets.recvfrom(1024)
                if incoming:
                    break
            except:
                print('\rWait', end='')
        # print(f'NEW: {get_seqNum(incoming)}, {check_flag_ack(incoming)}, {get_ack_num(incoming)}')
        if not corrupt(incoming):
            print(incoming)
            if (x + 1) == get_ackNum(incoming) and check_flag_ack(incoming):  # Incoming AckNum = x + 1, Ack
                seg.set_ackNum(get_seqNum(incoming) + 1)  # incoming SeqNum + 1
                seg.flags['A'] = 0b1
                self.sockets.sendto(seg.make_packet(''.encode()), (self.destination, self.port))
                self.sockets.connect((self.destination, self.port))
                print('Shaked!!')


if __name__ == '__main__':
    image = open('../imgs/select_me.bmp', 'rb')  # opens bitmap file
    p = Packet(image)
    p.make_packet()  # creates all packets to send to server with all headers
    print(len(p.packets))
    N = 1  # 4096
    MSS = 1000
    # N = args.N
    print(f'**** GB{N} ****')
    with socket(AF_INET, SOCK_DGRAM) as client_socket:
        sender = Sender(12000, gethostname(), client_socket)
        sender.handShake()

        T = 0
        st_clock = time.time()

        client_socket.setblocking(False)
        sender = Sender(12000, gethostname(), client_socket)  # create instance of Sender class
        done = False
        base = 0
        nextseqnum = 0
        rec_window = 4096
        rtt_time = 0.30
        dev_rtt = 0
        stamp_time = 0
        while not done:

            if rtt_time > 0.01:
                timeout = rtt_time + dev_rtt * 4

            if nextseqnum < base + rec_window:
                seg = Segment()
                seg.set_seqNum(nextseqnum)
                seg.set_head_len(15)
                sender.rdt_send(seg.make_packet(p.packets[nextseqnum // 1000]))
                stamp_time = time.time()
                if base == nextseqnum:
                    T = time.time()  # Start Timer
                nextseqnum += MSS
                print(
                    f'\n\rseq: {nextseqnum}, Base: {base}, RecW: {rec_window}\t T: {rtt_time * 1000 // 1}ms, STD: {dev_rtt * 1000 // 1}ms',
                    end='')

            if time_out(T):
                T = time.time()  # Reset Timer
                for i in range(base, min(nextseqnum, end_buff), MSS):
                    seg = Segment()
                    seg.set_seqNum(i)
                    seg.set_head_len(15)
                    sender.rdt_send(seg.make_packet(p.packets[i // 1000]))

            if sender.rdt_rcv():
                rtt = time.time() - stamp_time
                rtt_time = rtt_time * 0.875 + rtt * 0.125
                dev_rtt = dev_rtt * 0.75 + np.abs(rtt - rtt_time) * 0.25

                base = get_ackNum(sender.rcvpkt)
                rec_window = get_rec_window(sender.rcvpkt)
                if base != nextseqnum:
                    T = time.time()  # Reset Timer


            if nextseqnum // 1000 == 819:
                done = True
        sender.close()
    print(f"\nElapsed time: {time.time() - st_clock}")
