import sys
import socket
import threading

class UDProxy:
    def __init__(self, listen_ip, listen_port, forward_ip, forward_port):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.forward_ip = forward_ip
        self.forward_port = forward_port

        self.listen_socket = None
        self.forward_socket = None

    def initialize_proxy(self):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the listen socket to the specified IP and port
        self.listen_socket.bind((self.listen_ip, self.listen_port))

    def forward_data(self):
        print(f"Proxy started. Listening on {self.listen_ip}:{self.listen_port}. Forwarding to {self.forward_ip}:{self.forward_port}.")
        while True:
            data, address = self.listen_socket.recvfrom(1024)
            self.forward_socket.sendto(data, (self.forward_ip, self.forward_port))
            print(f"Forwarding data from {self.listen_ip}:{self.listen_port} to {self.forward_ip}:{self.forward_port}.")

            # Receive the response from the forward server
            response, forward_address = self.forward_socket.recvfrom(1024)

            # Forward the response back to the original sender
            self.listen_socket.sendto(response, address)
            print(f"Forwarding response from {self.forward_ip}:{self.forward_port} to {self.listen_ip}:{self.listen_port}.")

    def run(self):
        self.initialize_proxy()

        forward_thread = threading.Thread(target=self.forward_data)
        forward_thread.start()

        try:
            forward_thread.join()
        except KeyboardInterrupt:
            print("\nProxy terminated.")

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
