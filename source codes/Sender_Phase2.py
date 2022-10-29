from socket import *  # imports socket module to enable network communication


def seqnum_zero(receiverpacket):
    if receiverpacket[0] == 0:
        return True
    else:
        return False


def seqnum_one(receiverpacket):
    if receiverpacket[0] == 1:
        return True
    else:
        return False


class Packet:

    def __init__(self, data):

        self.packets = []   # file packet
        self.data = data

    def checksum(self, data):
        ch = data[0:2]

        for i in range(2, len(data), 2):
            a = int.from_bytes(data[i:i + 2], 'big') + int.from_bytes(ch, 'big')

            if a > 65535:
                a -= 65535

            ch = (~a).to_bytes(3, 'big', signed=True)
            ch = ch[1:]
        return ch

    def make_packet(self):

        i = 0  # initialize loop variable
        while True:
            skip = i * 1024  # skip variable holds number of bytes already stored
            self.data.seek(skip)  # skip over bytes already stored as packets
            chunk = self.data.read(1024)  # store 1024 bytes of file as a packet

            seqnum = i % 2

            chunk = chunk + seqnum.to_bytes(1, 'big') + len(chunk)

            ch = self.checksum(chunk)

            print(len(ch), len(chunk))

            senderpacket = chunk + ch
            i += 1  # increment loop variable
            self.packets.append(senderpacket)  # add packet to array
            if len(chunk) < 1024:  # once a packet is less than 1024 bytes, end of file reached, so break
                image.close()  # close bmp file
                break


class Sender:
    def __init__(self, port, destination, sockets, ):
        self.port = port  # server port number
        self.destination = destination  # server name
        self.sockets = sockets  # client socket
        self.packets = []  # packet array
        self.rcvpkt = []

    def socket_close(self):
        self.sockets.close()

    def receive_packet(self):
        self.rcvpkt, serveraddress = self.sockets.recvfrom(4)
        if self.rcvpkt:
            True
        else:
            False


if __name__ == '__main__':
    with socket(AF_INET, SOCK_DGRAM) as client_socket:
        s = Sender(12000, gethostname(), client_socket)  # create instance of Sender class

    image = open('../imgs/select_me.bmp', 'rb')  # opens bitmap file
    p = Packet(image)
    p.make_packet()

    states = ['w4zero', 'w4Ack0', 'w4zero', 'w4Ack1']
    state = states[0]

    for packet in p.packets:
        if state == states[0]:
            s.sockets.send(packet.encode())
            state = states[1]

        elif states == states[1]:
            if s.receive_packet() and (corrupt(rcvpkt) or seqnum_zero(s.rcvpkt)):
                s.sockets.send(packet.encode())
            elif s.receive_packet() and (not corrupt(rcvpkt)) and seqnum_one(s.rcvpkt):
                state = states[2]
        elif state == states[2]:
            s.sockets.send(packet.encode())
            state = states[3]
        elif state == states[3]:
            if s.receive_packet() and (corrupt(rcvpkt) or seqnum_zero(s.rcvpkt)):
                s.sockets.send(packet.encode())
            elif s.receive_packet() and (not corrupt(rcvpkt)) and seqnum_one(s.rcvpkt):
                state = states[0]
