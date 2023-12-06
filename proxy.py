# Description: Simple UDP Proxy
#
# Goal: To create a simple UDP proxy that forwards packets
# between a server and a client.

import sys
import socket
import threading

class Proxy:
    def __init__(self, server_address, server_port, client_address, client_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_address = client_address
        self.client_port = client_port

        self.server_socket = None
        self.client_socket = None

    def initialize_proxy(self):
        self.server_socket = socket.socket(socket.AF_INET6 if ':' in self.server_address else socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket = socket.socket(socket.AF_INET6 if ':' in self.client_address else socket.AF_INET, socket.SOCK_DGRAM)

        self.server_socket.bind((self.server_address, self.server_port))
        self.client_socket.bind((self.client_address, self.client_port))

    def forward_data(self, source_socket, destination_socket):
        while True:
            data, address = source_socket.recvfrom(1024)
            destination_socket.sendto(data, (self.client_address, self.client_port))

    def run(self):
        server_to_client_thread = threading.Thread(target=self.forward_data, args=(self.server_socket, self.client_socket))
        client_to_server_thread = threading.Thread(target=self.forward_data, args=(self.client_socket, self.server_socket))

        server_to_client_thread.start()
        client_to_server_thread.start()

        server_to_client_thread.join()
        client_to_server_thread.join()

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python proxy.py <server IP address> <server port> <client IP address> <client port>")
        sys.exit(1)

    server_address = sys.argv[1]
    server_port = int(sys.argv[2])
    client_address = sys.argv[3]
    client_port = int(sys.argv[4])

    proxy = Proxy(server_address, server_port, client_address, client_port)
    proxy.initialize_proxy()
    proxy.run()
