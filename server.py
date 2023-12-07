# Description: Reliable UDP socket server
#
# Goal: To create a reliable UDP socket server that can send acknowledgements and receive messages
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
        # Sets all variables for connection
        self.address = address
        self.port = port
        self.server_socket = None
        self.inputs = {}

    def initialize_server(self):
        # Sets up the socket for the server
        self.server_socket = socket.socket(socket.AF_INET6 if ':' in self.address else socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.address, self.port))
        print(f'Server listening on {self.address}:{self.port}...')
        self.inputs[self.server_socket.fileno()] = self.server_socket
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        # Handles the signal to close the server
        print('Closing server...')
        if self.server_socket:
            self.server_socket.close()
        sys.exit(0)

    def handle_received_message(self, data, client_address):
        # Handles the received message and sends an acknowledgment
        message = data.decode()
        print(f"Received message from {client_address}: {message}")

        # Extract sequence number from the message
        parts = message.split("|")
        sequence_number = parts[-1]

        # Generate acknowledgment with the same sequence number
        ack_message = f"{message.split('|ACK|')[0]}|ACK|{sequence_number}"
        self.server_socket.sendto(ack_message.encode(), client_address)
        print(f"Sent acknowledgment to {client_address}: {ack_message}")

    def run(self):
        # Runs the server
        while True:
            readable, _, _ = select.select(list(self.inputs.values()), [], [])
            for s in readable:
                if s is self.server_socket:
                    # Accept a new connection
                    data, client_address = s.recvfrom(1024)
                    self.handle_received_message(data, client_address)

if __name__ == '__main__':
    # Checks if the user has entered the correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python server.py <IPv4 or IPv6 address> <port>")
        sys.exit(1)

    # Sets the address and port for the server
    address = sys.argv[1]
    port = int(sys.argv[2])

    server_fsm = ServerFSM(address, port)
    server_fsm.initialize_server()
    server_fsm.run()
