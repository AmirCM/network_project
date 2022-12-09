import socket
import time
from socket import *  # imports socket module to enable network communication
import numpy as np
from TCP import *
import io

end_pointer = 4095


class Receiver:
    def __init__(self, port):
        self.sockets = socket(AF_INET, SOCK_DGRAM)  # Receiver socket
        self.dst_addr = None
        self.recv_pkt = None
        self.port = port

    def rdt_rcv(self) -> bool:
        self.recv_pkt, self.dst_addr = self.sockets.recvfrom(1024)
        if not corrupt(self.recv_pkt) and self.recv_pkt:
            return True
        return False

    def extract(self):
        pkt_len = get_head_len(self.recv_pkt)
        print(pkt_len, len(self.recv_pkt))
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
        print(len(self.buffer))
        with open('img.bmp', 'wb') as image:
            for i, p in enumerate(self.buffer):
                print(type(p))
                skip = i * 1000
                image.seek(skip)
                image.write(p)


def slide(Buffer: bytearray, pointer: int) -> bytearray:
    new = Buffer[pointer:] + bytearray([0x00] * pointer)
    return new


if __name__ == '__main__':
    application = App()
    out_order_buffer = {}

    buffer = bytearray([0x00] * 4096)

    r = Receiver(12000)
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
                if seqNum == next_AckNum:
                    data = r.extract()
                    buffer[buffer_pointer:buffer_pointer + len(data)] = data
                    buffer_pointer += len(data)
                    next_AckNum += len(data)
                    print(len(data))
                    while next_AckNum in out_order_buffer:
                        buffer_pointer += out_order_buffer[next_AckNum]
                        next_AckNum += out_order_buffer.pop(next_AckNum)

                    application.read(buffer, buffer_pointer)
                    buffer = slide(buffer, buffer_pointer)
                    remaining_buffer_size = buffer_pointer
                    buffer_pointer = 0
                elif seqNum < next_AckNum + remaining_buffer_size:
                    print('OUT OF ORDER')
                    data = r.extract()
                    loc = seqNum - next_AckNum
                    buffer[buffer_pointer + loc:] = data
                    out_order_buffer[buffer_pointer + loc] = len(data)
                    remaining_buffer_size = end_pointer - (buffer_pointer + loc + len(data)) + 1

                seg.reset_flags()
                seg.set_ackNum(next_AckNum)
                seg.flags['A'] = 0b1
                seg.set_rec_window(remaining_buffer_size)
                seg.set_head_len(15)
                pkt = seg.make_packet(''.encode())
                # print(f'window size = {pkt}')
                print(f'NA:{next_AckNum}')
                r.sockets.send(pkt)
            else:
                print('Blaaa')
                r.sockets.send(seg.make_packet(''.encode()))
        application.save()
