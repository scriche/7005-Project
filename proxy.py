import sys
import socket
import threading
import random
from threading import Timer
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

        self.listen_settings = {'drop': float(input(f"Enter the drop percentage to listener {self.listen_ip} (0 to 100): ")),
                               'delay': float(input(f"Enter the delay percentage to listener {self.listen_ip} (0 to 100): "))}

        self.forward_settings = {'drop': float(input(f"Enter the drop percentage to forwarder {self.forward_ip} (0 to 100): ")),
                                'delay': float(input(f"Enter the delay percentage to forwarder {self.forward_ip} (0 to 100): "))}

    def forward_data(self, data, source_address, apply_delay):
        # Get drop and delay percentages for the listener IP
        drop_chance_listen = self.listen_settings['drop']
        delay_chance_listen = self.listen_settings['delay']

        # Simulate drop based on user input percentages
        if random.uniform(0, 100) < drop_chance_listen:
            print(f"Simulating drop to {self.listen_ip}: Data not forwarded.")
            return

        # Simulate delay for listener
        if apply_delay and random.uniform(0, 100) < delay_chance_listen:
            time.sleep(5)  # Simulate delay by sleeping for 5 seconds
            print(f"Simulating delay to {self.listen_ip}: Data forwarded after delay.")

        # Forward data to the server
        self.forward_socket.sendto(data, (self.forward_ip, self.forward_port))
        print(f"Forwarding data from {self.listen_ip}:{self.listen_port} to {self.forward_ip}:{self.forward_port}.")

        # Get drop and delay percentages for the forward IP
        drop_chance_forward = self.forward_settings['drop']
        delay_chance_forward = self.forward_settings['delay']

        # Receive the response from the forward server
        try:
            response, _ = self.forward_socket.recvfrom(1024)

            # Simulate drop based on user input percentages
            if random.uniform(0, 100) < drop_chance_forward:
                print(f"Simulating drop to {self.listen_ip}: Response not forwarded.")
                return

            # Simulate delay for forwarder
            if random.uniform(0, 100) < delay_chance_forward:
                time.sleep(5)  # Simulate delay by sleeping for 5 seconds
                print(f"Simulating delay to {self.forward_ip}: Response forwarded after delay.")

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
            apply_delay = random.uniform(0, 100) < self.listen_settings['delay']
            threading.Thread(target=self.forward_data, args=(data, source_address, apply_delay)).start()

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
