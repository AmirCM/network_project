from socket import *  # imports socket module to enable network communication


class Receiver:
    def __init__(self, port, sockets, image):
        self.port = port  # server port number
        self.sockets = sockets  # server socket
        self.image = image
        self.packets = []
        self.socket_bind()

    def make_file(self):
        # self.image = open('received_image.bmp', 'wb')  # opens bitmap file
        i = 0  # initialize loop variable
        self.packets = []
        while True:
            incoming, address = self.sockets.recvfrom(1024)
            self.packets.append(incoming)  # packet to array
            print(len(incoming))
            if len(incoming) < 1024:
                break

        for i, p in enumerate(self.packets):
            skip = i * 1024  # skip variable holds number of bytes already stored
            self.image.seek(skip)  # skip over bytes already stored as packets
            self.image.write(p)  # writing packets to file
            i += 1  # increment loop variable
        self.image.close()

    def socket_bind(self):
        self.sockets.bind(('', self.port))  # binds to the socket


if __name__ == '__main__':
    r = Receiver(12000, socket(AF_INET, SOCK_DGRAM), open('../imgs/received_image.bmp', 'wb'))
    r.make_file()

