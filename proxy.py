import sys
import socket
import threading
import random
import time

class UDProxy:
    def __init__(self, listen_ip, listen_port, forward_ip, forward_port):
        # Sets all variables for connection
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.forward_ip = forward_ip
        self.forward_port = forward_port

        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.listen_socket.bind((self.listen_ip, self.listen_port))
        self.forward_socket.settimeout(2.0)

        self.listen_settings = self.get_user_settings(f"Enter the settings for listener {self.listen_ip}: ")
        self.forward_settings = self.get_user_settings(f"Enter the settings for forwarder {self.forward_ip}: ")

    def get_user_settings(self, prompt):
        # Gets the user settings for the proxy
        settings = {
            'drop': float(input(f"{prompt}Drop percentage (0 to 100): ")),
            'delay': float(input(f"{prompt}Delay percentage (0 to 100): "))
        }
        return settings

    def apply_delay(self, chance):
        # Applies a delay to the message
        if random.uniform(0, 100) < chance:
            delay = 4
            time.sleep(delay)
            return True
        return False

    def simulate_action(self, action_type, chance, message):
        # Simulates an action delay or drop
        if random.uniform(0, 100) < chance:
            print(f"Simulating {action_type} to {self.listen_ip}: {message}.")
            return True
        return False

    def forward_data(self, data, source_address):
        # Forwards the data to the forwarder
        drop_chance_listen = self.listen_settings['drop']
        delay_chance_listen = self.listen_settings['delay']

        if self.simulate_action("drop", drop_chance_listen, "Data not forwarded"):
            return

        if self.apply_delay(delay_chance_listen):
            print(f"Simulating delay to {self.listen_ip}: Data forwarded after delay.")

        # Forward the data to the forwarder
        threading.Thread(target=self.forward_response, args=(data, source_address)).start()

    def forward_response(self, data, source_address):
        # Forwards the response to the listener
        self.forward_socket.sendto(data, (self.forward_ip, self.forward_port))
        print(f"Forwarding data from {self.listen_ip}:{self.listen_port} to {self.forward_ip}:{self.forward_port}.")

        drop_chance_forward = self.forward_settings['drop']
        delay_chance_forward = self.forward_settings['delay']

        try:
            # Receive response from the forwarder
            response, _ = self.forward_socket.recvfrom(1024)

            if self.simulate_action("drop", drop_chance_forward, "Response not forwarded"):
                return

            if self.apply_delay(delay_chance_forward):
                print(f"Simulating delay to {self.forward_ip}: Response forwarded after delay.")

            threading.Thread(target=self.forward_listener, args=(response, source_address)).start()

        except socket.timeout:
            print("Timeout occurred while waiting for data.")

    def forward_listener(self, response, source_address):
        # Forwards the response to the listener
        self.listen_socket.sendto(response, source_address)
        print(f"Forwarded response to {self.listen_ip}:{self.listen_port}.")

    def run(self):
        # Runs the proxy
        print(f"Proxy started. Listening on {self.listen_ip}:{self.listen_port}. Forwarding to {self.forward_ip}:{self.forward_port}.")

        while True:
            data, source_address = self.listen_socket.recvfrom(1024)
            threading.Thread(target=self.forward_data, args=(data, source_address)).start()

if __name__ == '__main__':
    # Check for correct number of arguments
    if len(sys.argv) != 5:
        print("Usage: python udp_proxy.py <listen IP> <listen port> <forward IP> <forward port>")
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    forward_ip = sys.argv[3]
    forward_port = int(sys.argv[4])

    udp_proxy = UDProxy(listen_ip, listen_port, forward_ip, forward_port)
    udp_proxy.run()
