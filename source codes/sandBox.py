import socket
import time
from socket import *  # imports socket module to enable network communication
from TCP import *

with socket(AF_INET, SOCK_DGRAM) as client_socket:
    client_socket.bind(('', 12000))
    while True:
        incoming, dst_addr = client_socket.recvfrom(1024)
        print('First', incoming)
        if not corrupt(incoming):
            break
    print(check_flag_sync(incoming))
    if check_flag_sync(incoming):
        print(incoming)
        seq_num = get_seqNum(incoming)
        packet = Segment()
        packet.header['ack_num'] = seq_num + 1
        packet.header['seq_num'] = 10
        packet.flags['A'] = 0b1
        packet.flags['S'] = 0b1
        client_socket.sendto(packet.make_packet(''.encode()), dst_addr)
        print('Shacked!!!!!')
