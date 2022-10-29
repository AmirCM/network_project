import socket
import sys

states = ['w4zero', 'w4Ack0', 'w4zero', 'w4Ack1']
state = states[0]       # On rdt_send(data) call
if __name__ == '__main__':
    if state == states[0]:
        if called:
            sndpkt = make_pkt(0, data, checksum)
            udt_send(sndpkt)
            state = states[1]
    elif states == states[1]:
        if rdt_rcv(rcvpkt) and (corrupt(rcvpkt) or is_ack(rcvpkt, 0)):
            udt_send(sndpkt)
        elif rdt_rcv(rcvpkt) and (not corrupt(rcvpkt)) and is_ack(rcvpkt, 1) == 0:
            state = states[2]
    elif state == states[2]:
        if called:
            sndpkt = make_pkt(1, data, checksum)
            udt_send(sndpkt)
            state = states[3]
    elif state == states[3]:
        if rdt_rcv(rcvpkt) and (corrupt(rcvpkt) or is_ack(rcvpkt, 0)):
            udt_send(sndpkt)
        elif rdt_rcv(rcvpkt) and (not corrupt(rcvpkt)) and is_ack(rcvpkt, 1) == 1:
            state = states[0]


