import sys
import socket
import threading
import random

class UDProxy:
    def __init__(self, listen_ip, listen_port, forward_ip, forward_port):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.forward_ip = forward_ip
        self.forward_port = forward_port

        self.listen_socket = None
        self.forward_socket = None
        self.drop_chance_to_server = 0
        self.delay_chance_to_server = 0
        self.drop_chance_to_client = 0
        self.delay_chance_to_client = 0

    def initialize_proxy(self):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the listen socket to the specified IP and port
        self.listen_socket.bind((self.listen_ip, self.listen_port))

        # Ask for user input for drop and delay percentages
        self.drop_chance_to_server = float(input("Enter the drop percentage to server (0 to 100): "))
        self.delay_chance_to_server = float(input("Enter the delay percentage to server (0 to 100): "))
        self.drop_chance_to_client = float(input("Enter the drop percentage to client (0 to 100): "))
        self.delay_chance_to_client = float(input("Enter the delay percentage to client (0 to 100): "))

    def forward_data(self):
        print(f"Proxy started. Listening on {self.listen_ip}:{self.listen_port}. Forwarding to {self.forward_ip}:{self.forward_port}.")

        while True:
            try:
                # Set a timeout for receiving data (in seconds)
                data, address = self.listen_socket.recvfrom(1024)

                # Simulate drop and delay based on user input percentages
                if random.uniform(0, 100) > self.drop_chance_to_server:
                    # Forward data to the server
                    self.forward_socket.sendto(data, (self.forward_ip, self.forward_port))
                    print(f"Forwarding data from {self.listen_ip}:{self.listen_port} to {self.forward_ip}:{self.forward_port}.")

                    # Simulate delay
                    if random.uniform(0, 100) > self.delay_chance_to_server:
                        # Receive the response from the forward server with a timeout
                        self.forward_socket.settimeout(2.0)  # Adjust the timeout as needed
                        response, forward_address = self.forward_socket.recvfrom(1024)
                        print(f"Received response from {self.forward_ip}:{self.forward_port}. Forwarding to {self.listen_ip}:{self.listen_port}.")

                        # Forward the response back to the original sender
                        self.listen_socket.sendto(response, address)
                        print(f"Forwarded response to {self.listen_ip}:{self.listen_port}.")
                    else:
                        print(f"Simulating delay to server: Data not forwarded immediately.")
                else:
                    print(f"Simulating drop to server: Data not forwarded.")

            except socket.timeout:
                # Handle timeout (e.g., print a message)
                print("Timeout occurred while waiting for data.")

    def run(self):
        self.initialize_proxy()
        self.forward_data()

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python udp_proxy.py <listen IP> <listen port> <forward IP> <forward port>")
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    forward_ip = sys.argv[3]
    forward_port = int(sys.argv[4])

    udp_proxy = UDProxy(listen_ip, listen_port, forward_ip, forward_port)
    udp_proxy.run()
