import socket
import time
from socket import *  # imports socket module to enable network communication
import numpy as np
from TCP import *
import argparse

end_pointer = 40095


class Receiver:
    def __init__(self, port, loss_probability):
        self.sockets = socket(AF_INET, SOCK_DGRAM)  # Receiver socket
        self.dst_addr = None
        self.recv_pkt = None
        self.port = port
        self.loss_probability = loss_probability

    def rdt_rcv(self) -> bool:
        try:
            self.recv_pkt = self.sockets.recv(4095)
        except:
            return False
        if np.random.binomial(1, self.loss_probability):
            return False
        if not corrupt(self.recv_pkt) and self.recv_pkt:
            return True
        return False

    def extract(self):
        pkt_len = get_head_len(self.recv_pkt)
        return self.recv_pkt[pkt_len:]

    def listen(self):
        while True:
            incoming, dst_addr = self.sockets.recvfrom(1024)
            if not corrupt(incoming):
                break
        if check_flag_sync(incoming):
            seq_num = get_seqNum(incoming)
            packet = Segment()
            packet.header['ack_num'] = seq_num + 1
            packet.header['seq_num'] = 10
            packet.flags['A'] = 0b1
            packet.flags['S'] = 0b1
            pkt = packet.make_packet(''.encode())
            self.sockets.sendto(pkt, dst_addr)
        else:
            return False

        while True:
            incoming, dst_addr = self.sockets.recvfrom(1024)
            if not corrupt(incoming):
                break
        if check_flag_ack(incoming) and get_ackNum(incoming) == 11:
            print('Connection successful')
            self.sockets.connect(dst_addr)
            return True


class App:
    def __init__(self):
        self.buffer = []

    def read(self, tcp_buffer: bytearray, last_byte: int):
        data = tcp_buffer[:last_byte]
        self.buffer.append(data)

    def save(self):
        with open('img.bmp', 'wb') as image:
            for i, p in enumerate(self.buffer):
                skip = i * 1000
                image.seek(skip)
                image.write(p)


def slide(Buffer: bytearray, pointer: int) -> bytearray:
    new = Buffer[pointer:] + bytearray([0x00] * pointer)
    # print(f'\t NEW: {len(Buffer[pointer:])} {len(new)}, {pointer}')
    return new


if __name__ == '__main__':
    application = App()
    out_order_buffer = {}
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', type=float, required=False)
    args = arg_parser.parse_args()
    p = 0
    if args.p:
        p = args.p

    buffer = bytearray([0x00] * end_pointer)

    r = Receiver(12000, p)
    r.sockets.bind(('', 12000))

    buffer_pointer = 0
    next_AckNum = 0

    remaining_buffer_size = end_pointer - buffer_pointer + 1
    if r.listen():
        seg = Segment()
        while True:
            if r.rdt_rcv():
                if check_flag_f(r.recv_pkt):
                    seg.reset_flags()
                    seg.flags['A'] = 0b1
                    seg.flags['F'] = 0b1
                    r.sockets.send(seg.make_packet(''.encode()))
                    break

                seqNum = get_seqNum(r.recv_pkt)
                data = r.extract()

                if seqNum == next_AckNum and (len(data) <= remaining_buffer_size or len(data) <= 1000):
                    buffer[buffer_pointer:buffer_pointer + len(data)] = data
                    buffer_pointer += len(data)
                    next_AckNum += len(data)

                    while next_AckNum in out_order_buffer:
                        buffer_pointer += out_order_buffer[next_AckNum]
                        next_AckNum += out_order_buffer.pop(next_AckNum)

                    application.read(buffer, buffer_pointer)
                    buffer = slide(buffer, buffer_pointer)
                    remaining_buffer_size = buffer_pointer
                    buffer_pointer = 0
                elif len(data) <= remaining_buffer_size and (
                        len(data) + seqNum - next_AckNum) < remaining_buffer_size and seqNum > next_AckNum:
                    print(
                        f'\n\rOUT of ORDER {remaining_buffer_size}, {buffer_pointer}, {seqNum}, {next_AckNum}, {len(data)}')
                    loc = seqNum - next_AckNum
                    buffer[buffer_pointer + loc:len(data)] = data
                    out_order_buffer[buffer_pointer + loc] = len(data)
                    remaining_buffer_size = end_pointer - (buffer_pointer + loc + len(data)) + 1
                seg.reset_flags()
                seg.set_ackNum(next_AckNum)
                seg.flags['A'] = 0b1
                seg.set_rec_window(remaining_buffer_size)
                seg.set_head_len(15)
                try:
                    r.sockets.send(seg.make_packet(''.encode()))
                    print(f'\rnextAck:{next_AckNum}, Seq:{seqNum}', end='')
                except:
                    print(f'\rNA:{seg.header}', end='')
                    input('?')

            else:
                if seg.flags['A'] == 0b1:
                    print(f'\tDA:{next_AckNum}', end='')
                    r.sockets.send(seg.make_packet(''.encode()))
        application.save()
