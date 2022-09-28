from socket import *   # imports socket module to enable network communication


def make_packet(array):
    image = open('../imgs/image.bmp', 'rb')   # opens bitmap file
    i = 0                  # initialize loop variable
    while True:
        skip = i*1024      # skip variable holds number of bytes already stored
        image.seek(skip)       # skip over bytes already stored as packets
        data = image.read(1024)  # store 1024 bytes of file as a packet
        i += 1             # increment loop variable
        array.append(data)     # add packet to array
        if len(data) < 1024:   # once a packet is less than 1024 bytes, end of file reached, so break
            break
    image.close()
    return array           # return array of packets


if __name__ == '__main__':
    # sets the serverName variable to the server's IP Address
    serverName = "192.168.68.126"

    # serverPort variable set to 12000
    serverPort = 12000

    # creates the client's socket, AF_INET indicates network is using IPv4, SOCK_DGRAM specifies a UDP socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    packet_array = []           # create array for packets

    make_packet(packet_array)   # call function to parse bmp file

    for packet in packet_array:
        clientSocket.sendto(packet, (serverName, serverPort))   # individually sends each packet in array

    # closes the socket, terminating the process
    clientSocket.close()
