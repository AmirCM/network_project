from socket import *  # imports socket module to enable network communication


def extract_sender_data(data):
    sender_packet_length = len(data)
    return data[0: (sender_packet_length - 1)]


class Receiver:
    def __init__(self, port, sockets, data):
        self.port = port  # Receiver port number
        self.sockets = sockets  # Receiver socket
        self.packets = []  # Receiver packets
        self.socket_bind()  # Receiver bind to socket
        self.data = data

    # Extract data from received sender packet
    def extract_data(self, data):
        sender_packet_length = len(data)
        return data[0:(sender_packet_length - 5)]

    # Function to generate checksum
    def checksum(self, data):
        ch = data[0:2]

        for i in range(2, len(data), 2):
            a = int.from_bytes(data[i:i + 2], 'big') + int.from_bytes(ch, 'big')

            if a > 65535:
                a -= 65535

            ch = (~a).to_bytes(3, 'big', signed=True)
            ch = ch[1:]
        return ch

    # Function to check if the received packet has sequence number 0 or 1
    def check_sequence_number(self, senderpacket):
        if senderpacket.data[0:1] == '1':
            return True
        if senderpacket.data[0:1] == '0':
            return False

    # Function to check if sender packet is corrupt
    def corrupt_check(self, senderpacket, checksum):
        sender_packet_length = len(senderpacket)
        if checksum(senderpacket[0:(sender_packet_length - 1)]) == senderpacket[
                                                                   (sender_packet_length - 1):sender_packet_length]:
            return True
        else:
            return False

    # Function used to make image file for Phase 2
    def make_file(self, path):
        with open(path, 'wb') as image:
            for i, p in enumerate(self.packets):
                skip = i * 1024  # skip variable holds number of bytes already stored
                image.seek(skip)  # skip over bytes already stored as packets
                image.write(p)  # writing packets to file

    # Function to make packet that will be returned to sender
    def make_packet(self, data, checksum):
        i = 0
        sequence_num = i % 2
        chunk = self.data.read(1024)
        chunk += sequence_num.to_bytes(1, 'big')
        receiverpacket = str(int(sequence_num)).encode() + data + checksum
        return receiverpacket

    # Function to initialize receiver and begin listening
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
    r = Receiver(12000, socket(AF_INET, SOCK_DGRAM))  # create instance of Receiver class
    r.start()  # Start server & listening for incoming data

    # State 1
    # If the received packet is corrupt or sequence with ‘1’ it sends acknowledgment with sequence number ‘1’ to it which tells the sender that the packet sent was not in order.
    if corrupt_check(senderpacket) or check_sequence_number(senderpacket) == 'True':

    # If the packet is not corrupt and has sequence number ‘0’ the receiver extracts the data and sends acknowledgment with the sequence ‘0’. It moves to the next state.
    if not corrupt_check(senderpacket) and check_sequence_number(senderpacket) == 'False':

    # State 2
    # If the received packet is corrupt or sequence with ‘0’ it sends acknowledgment with sequence number ‘0’ to it which tells the sender that the packet sent was not in order.
    if corrupt_check(senderpacket) or check_sequence_number(senderpacket) == 'False':

    # If the packet is not corrupt and has sequence number ‘1’ the receiver extracts the data and sends acknowledgment with the sequence ‘1’. It moves to the next state.
    if not corrupt_check(senderpacket) and check_sequence_number(senderpacket) == 'True':

    r.make_file('../imgs/received_image.bmp')  # rebuild & save the image
