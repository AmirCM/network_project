import socket

if __name__ == '__main__':
    print("Server Running!!!")
    my_host = ''
    my_port = 13333

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((my_host, my_port))

        while True:
            incoming, addr = server_socket.recvfrom(1024)
            if not incoming:
                break

            server_socket.sendto(incoming, addr)
            print(f"Incoming msg from {addr} connection, msg: {incoming.decode()}")

            if incoming.decode() == "exit":
                break
    print("Server is terminated !!!")



