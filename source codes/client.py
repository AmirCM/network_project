import socket
import sys

ACK = True
states = ['w4zero', 'w4one']
state = states[0]
if __name__ == '__main__':
    if state == states[0]:
        if rdt_rcv(rcvpkt) and (corrupt(rcvpkt) or get_seq(rcvpkt) == 1):
            if oncethru == 1
                udt_send(sndpkt)
        elif rdt_rcv(rcvpkt) and (not corrupt(rcvpkt)) and get_seq(rcvpkt) == 0:
            extract(rcvpkt, data)
            deliver_data(data)
            sndpkt = make_pkt(ACK,0,checksum)
            udt_send(sndpkt)
            oncethru = 1
            state = states[1]       # Next State
    elif states == states[1]:
        if rdt_rcv(rcvpkt) and (corrupt(rcvpkt) or get_seq(rcvpkt) == 0):
            udt_send(sndpkt)
        elif rdt_rcv(rcvpkt) and (not corrupt(rcvpkt)) and get_seq(rcvpkt) == 1:
            extract(rcvpkt, data)
            deliver_data(data)
            sndpkt = make_pkt(ACK, 1, checksum)
            udt_send(sndpkt)
            state = states[0]       # Next State

