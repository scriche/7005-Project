import sys
import socket
import threading
import random
import time

class UDProxy:
    def __init__(self, listen_ip, listen_port, forward_ip, forward_port):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.forward_ip = forward_ip
        self.forward_port = forward_port

        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.listen_socket.bind((self.listen_ip, self.listen_port))
        self.forward_socket.settimeout(2.0)

        self.drop_chance_to_client = float(input("Enter the drop percentage to client (0 to 100): "))
        self.delay_chance_to_client = float(input("Enter the delay percentage to client (0 to 100): "))

    def forward_data(self, data, source_address):
        # Simulate drop based on user input percentages
        if source_address[0] == self.forward_ip and source_address[1] == self.forward_port:
            if random.uniform(0, 100) < self.drop_chance_to_client:
                print(f"Simulating drop to client: Data not forwarded.")
                return

        # Forward data to the server
        self.forward_socket.sendto(data, (self.forward_ip, self.forward_port))
        print(f"Forwarding data from {self.listen_ip}:{self.listen_port} to {self.forward_ip}:{self.forward_port}.")

        # Simulate delay
        if source_address[0] == self.forward_ip and source_address[1] == self.forward_port and random.uniform(0, 100) < self.delay_chance_to_client:
            time.sleep(5)  # Simulate delay by sleeping for 5 seconds
            print(f"Simulating delay to client: Data forwarded after delay.")

        # Receive the response from the forward server
        try:
            response, _ = self.forward_socket.recvfrom(1024)
            print(f"Received response from {self.forward_ip}:{self.forward_port}. Forwarding to {self.listen_ip}:{self.listen_port}.")

            # Forward the response back to the original sender
            self.listen_socket.sendto(response, source_address)
            print(f"Forwarded response to {self.listen_ip}:{self.listen_port}.")

        except socket.timeout:
            # Handle timeout (e.g., print a message)
            print("Timeout occurred while waiting for data.")

    def run(self):
        print(f"Proxy started. Listening on {self.listen_ip}:{self.listen_port}. Forwarding to {self.forward_ip}:{self.forward_port}.")

        while True:
            data, source_address = self.listen_socket.recvfrom(1024)
            threading.Thread(target=self.forward_data, args=(data, source_address)).start()

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

