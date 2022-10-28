from socket import *  # imports socket module to enable network communication

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

            chunk += seqnum.to_bytes(1, 'big')

            ch = self.checksum(chunk)

            print(len(ch), len(chunk))

            senderpacket = chunk + ch
            i += 1  # increment loop variable
            self.packets.append(senderpacket)  # add packet to array
            if len(chunk) < 1024:  # once a packet is less than 1024 bytes, end of file reached, so break
                image.close()  # close bmp file
                break


class Sender:
    def __init__(self, port, destination, sockets):
        self.port = port  # server port number
        self.destination = destination  # server name
        self.sockets = sockets  # client socket
        self.packets = []  # packet array

    def socket_close(self):
        self.sockets.close()


if __name__ == '__main__':
    # with socket(AF_INET, SOCK_DGRAM) as client_socket:
      #   s = Sender(12000, gethostname(), client_socket)  # create instance of Sender class

    image = open('../imgs/select_me.bmp', 'rb')  # opens bitmap file

    p = Packet(image)

    p.make_packet()  # call function to parse bmp file into packets

   # for packet in p.packets:  # loop through packet array and individually send to receiver
    #    s.sockets.sendto(packet, (s.destination, s.port))
            # print(checksum(packet))

