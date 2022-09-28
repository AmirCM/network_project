from socket import *  # imports socket module to enable network communication


class Receiver:
    def __init__(self, port, sockets, image):
        self.port = port  # server port number
        self.sockets = sockets  # server socket
        self.image = image

    def make_file(self):
        self.image = open('received_image.bmp', 'wb')  # opens bitmap file
        i = 0  # initialize loop variable
        while True:
            incoming, address = self.sockets.recvfrom(1024)
            self.packets.append(incoming)  # packet to array
            if not incoming:
                break

        while True:
            skip = i * 1024  # skip variable holds number of bytes already stored
            self.image.seek(skip)  # skip over bytes already stored as packets
            self.image.write(incoming)  # writing packets to file
            i += 1  # increment loop variable
            if len(incoming) < 1024:  # once a packet is less than 1024 bytes, end of file reached, so break
                self.image.close()  # close bmp file
                break

    def socket_bind(self):
        self.sockets.bind(('', self.port))  # binds to the socket


if __name__ == '__main__':
    r = Receiver(12000, socket(AF_INET, SOCK_DGRAM), open('received_image.bmp', 'x'))
    r.socket_bind()
    r.make_file()
    print(r.image)

