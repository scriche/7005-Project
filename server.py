# Description: Reliable UDP socket server
#
# Goal: To create a reliable UDP socket server that can send and receive messages
# just like a TCP socket server but with UDP
#
# UDP socket server reads from a UDP socket and writes to console
# if it receives a message from a client then it sends an acknowledgment back
# to the client to establish a connection

import sys
import socket
import select
import signal

class ServerFSM:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.server_socket = None
        self.inputs = []

    def initialize_server(self):
        self.server_socket = socket.socket(socket.AF_INET6 if ':' in self.address else socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.address, self.port))
        print(f'Server listening on {self.address}:{self.port}...')
        self.inputs.append(self.server_socket)
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print('Closing server...')
        if self.server_socket:
            self.server_socket.close()
        sys.exit(0)

    def handle_received_message(self, data, client_address):
        message = data.decode()
        print(f"Received message from {client_address}: {message}")

    def run(self):
        while True:
            data, client_address = self.server_socket.recvfrom(1024)
            self.handle_received_message(data, client_address)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python server.py <IPv4 or IPv6 address> <port>")
        sys.exit(1)

    address = sys.argv[1]
    port = int(sys.argv[2])

    server_fsm = ServerFSM(address, port)
    server_fsm.initialize_server()
    server_fsm.run()