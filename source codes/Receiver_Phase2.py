from socket import *  # imports socket module to enable network communication


class Receiver:
    def __init__(self, port, sockets):
        self.port = port  # Receiver port number
        self.sockets = sockets  # Receiver socket
        self.packets = []  # Receiver packets
        self.socket_bind()  # Receiver bind to socket

    def make_file(self, path):
        with open(path, 'wb') as image:
            for i, p in enumerate(self.packets):
                skip = i * 1024  # skip variable holds number of bytes already stored
                image.seek(skip)  # skip over bytes already stored as packets
                image.write(p)  # writing packets to file

    def start(self):
        self.packets = []
        while True:
            incoming, address = self.sockets.recvfrom(1024)
            self.packets.append(incoming)  # packet to array
            print(len(incoming))
            if len(incoming) < 1024:
                break

    def socket_bind(self):
        self.sockets.bind(('', self.port))  # binds to the socket


if __name__ == '__main__':
    r = Receiver(12000, socket(AF_INET, SOCK_DGRAM))  # opens bitmap file
    r.start()
    r.make_file('../imgs/received_image.bmp')
