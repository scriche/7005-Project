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

        def receive_data():
            while True:
                data, address = self.listen_socket.recvfrom(1024)
                if data:
                    self.forward_socket.sendto(data, (self.forward_ip, self.forward_port))
                    print(f"Forwarding data from {self.listen_ip}:{self.listen_port} to {self.forward_ip}:{self.forward_port}.")

        def send_response():
            while True:
                response, forward_address = self.forward_socket.recvfrom(1024)
                print(f"Received response from {self.forward_ip}:{self.forward_port}. Forwarding to {self.listen_ip}:{self.listen_port}.")
                self.listen_socket.sendto(response, (self.listen_ip, self.listen_port))
                print(f"Forwarded response to {self.listen_ip}:{self.listen_port}.")

        # Start separate threads for sending and receiving
        receive_thread = threading.Thread(target=receive_data)
        send_thread = threading.Thread(target=send_response)

        receive_thread.start()
        send_thread.start()

        # Wait for both threads to finish (Ctrl+C will terminate the proxy)
        receive_thread.join()
        send_thread.join()

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python udp_proxy.py <listen IP> <listen port> <forward IP> <forward port>")
        sys.exit(1)

    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    forward_ip = sys.argv[3]
    forward_port = int(sys.argv[4])

    udp_proxy = UDProxy(listen_ip, listen_port, forward_ip, forward_port)
    udp_proxy.initialize_proxy()
    udp_proxy.forward_data()
