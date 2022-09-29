from socket import *  # imports socket module to enable network communication


class Sender:
    def __init__(self, port, destination, sockets, packets):
        self.port = port  # server port number
        self.destination = destination  # server name
        self.sockets = sockets  # client socket
        self.packets = packets  # packet array

    def make_packet(self):
        image = open('../imgs/image.bmp', 'rb')  # opens bitmap file
        i = 0  # initialize loop variable
        while True:
            skip = i * 1024  # skip variable holds number of bytes already stored
            image.seek(skip)  # skip over bytes already stored as packets
            data = image.read(1024)  # store 1024 bytes of file as a packet
            i += 1  # increment loop variable
            self.packets.append(data)  # add packet to array
            if len(data) < 1024:  # once a packet is less than 1024 bytes, end of file reached, so break
                image.close()     # close bmp file
                break

    def socket_close(self):
        self.sockets.close()


if __name__ == '__main__':
    with socket(AF_INET, SOCK_DGRAM) as client_socket:
        s = Sender(12000, gethostname(), client_socket, [])  # create instance of Sender class

        s.make_packet()  # call function to parse bmp file into packets

        for packet in s.packets:  # loop through packet array and individually send to receiver
            s.sockets.sendto(packet, (s.destination, s.port))
        s.sockets.sendto("exit".encode(), (s.destination, s.port))

