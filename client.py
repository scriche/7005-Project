# Description: Reliable UDP socket client
#
# Goal: To create a reliable UDP socket client that can send messages
# to the UDP server created in the server script.

import sys
import socket
import time

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = None
        self.sequence_number = 0
        self.MAX_RETRIES = 5
        self.last_acknowledged_sequence = -1

    def initialize_client(self):
        self.client_socket = socket.socket(socket.AF_INET6 if ':' in self.server_address else socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, message):
        self.sequence_number += 1
        formatted_message = f"{message}|ACK|{self.sequence_number}"

        if self.sequence_number > self.last_acknowledged_sequence:
            retries = 0
            while retries < self.MAX_RETRIES:
                self.client_socket.sendto(formatted_message.encode(), (self.server_address, self.server_port))
                print(f"Sent message to {self.server_address}:{self.server_port}: {message} (Seq: {self.sequence_number})")

                # Set a timeout for receiving acknowledgment
                self.client_socket.settimeout(2)

                try:
                    # Receive acknowledgment from the server
                    ack_message, _ = self.client_socket.recvfrom(1024)

                    # Check if the acknowledgment has the correct sequence number
                    ack_sequence_number = int(ack_message.decode().split('|')[-1])

                    if ack_sequence_number == self.last_acknowledged_sequence:
                        print(f"Received acknowledgment from {self.server_address}:{self.server_port}: {ack_message.decode()}")
                        break  # Exit the loop if acknowledgment is received

                    print(f"Ignored acknowledgment with incorrect or outdated sequence number: {ack_sequence_number}")

                except socket.timeout:
                    print(f"Timed out. Retrying ({retries + 1}/{self.MAX_RETRIES})...")
                    retries += 1
        else:
            print(f"Ignoring message with sequence number {self.sequence_number} (already acknowledged).")

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