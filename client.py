# Description: Reliable UDP socket client
#
# Goal: To create a reliable UDP socket client that can send messages
# to the UDP server created in the server script.

import sys
import socket

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = None

    def initialize_client(self):
        self.client_socket = socket.socket(socket.AF_INET6 if ':' in self.server_address else socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, message):
        self.client_socket.sendto(message.encode(), (self.server_address, self.server_port))

    def run(self):
        try:
            while True:
                message = input("Enter a message (or 'exit' to quit): ")
                if message.lower() == 'exit':
                    break
                self.send_message(message)
        except KeyboardInterrupt:
            print("\nCtrl+C received. Exiting gracefully.")
        finally:
            self.client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python client.py <server IP address> <server port>")
        sys.exit(1)

    server_address = sys.argv[1]
    server_port = int(sys.argv[2])

    client = Client(server_address, server_port)
    client.initialize_client()
    client.run()
