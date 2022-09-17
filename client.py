import socket
import sys

if __name__ == '__main__':
    host_name = socket.gethostname()
    server_port = 13333
    outgoing_msg = sys.argv[1].encode()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(outgoing_msg, (host_name, server_port))
        echo = client_socket.recv(2048)

        print(f"ECHO from server => {echo.decode()}")

