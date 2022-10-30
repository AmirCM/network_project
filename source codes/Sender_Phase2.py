from socket import *  # imports socket module to enable network communication


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


class Sender:
    def __init__(self, port: int, destination, sockets: socket):
        self.rcvpkt = None
        self.port = port  # server port number
        self.destination = destination  # server name
        self.sockets = sockets  # client socket
        self.packets = []  # packet array

    def has_seqnum(self, seq_num: int) -> bool:
        if int.from_bytes(self.rcvpkt[-3], 'big') == seq_num:
            return True
        return False

    def rdt_rcv(self):
        self.rcvpkt = self.sockets.recv(6)  # 1 Data, 2 len, 1 seq, 2 ch thus 6 Bytes
        if self.rcvpkt:
            return True
        return False

    def corrupt(self):
        ch = checksum(self.rcvpkt[:-2])  # Compute ch on the incoming pkt
        if ch == self.rcvpkt[-2:]:  # Compare ch to the incoming pkt ch
            return True
        return False

    def rdt_send(self, data):
        self.sockets.sendto(data, (self.destination, self.port))



if __name__ == '__main__':
    states = ['w4zero', 'w4Ack0', 'w4zero', 'w4Ack1']
    state = states[0]

    with socket(AF_INET, SOCK_DGRAM) as client_socket:
        s = Sender(12000, gethostname(), client_socket)  # create instance of Sender class

        image = open('../imgs/select_me.bmp', 'rb')  # opens bitmap file
        p = Packet(image)
        p.make_packet()                              # creates all packets to send to server with all headers

        for packet in p.packets:
            if state == states[0]:
                s.rdt_send(packet)
                state = states[1]

            elif states == states[1]:
                if s.rdt_rcv() and ((s.corrupt()) or s.has_seqnum(0)):
                    s.sockets.send(packet.encode())
                elif s.rdt_rcv() and (not s.corrupt()) and s.has_seqnum(1):
                    state = states[2]

            elif state == states[2]:
                s.rdt_send(packet)
                state = states[3]

            elif state == states[3]:
                if s.rdt_rcv() and ((s.corrupt()) or s.has_seqnum(0)):
                    s.sockets.send(packet.encode())
                elif s.rdt_rcv() and (not s.corrupt()) and s.has_seqnum(1):
                    state = states[0]
