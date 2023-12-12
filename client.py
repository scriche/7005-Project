# Description: Reliable UDP socket client
#
# Goal: To create a reliable UDP socket client that can send messages
# to the UDP proxy and receive acknowledgments from the UDP proxy.

import sys
import socket
import matplotlib.pyplot as plt

class Client:
    def __init__(self, server_address, server_port):
        # Sets all variable for connection
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = None
        self.sequence_number = 0
        self.MAX_RETRIES = 5
        self.sent_packets = 0
        self.received_packets = 0
        self.packet_history = []

    def initialize_client(self):
        # Sets up the socket for the client
        address_family = socket.AF_INET6 if ':' in self.server_address else socket.AF_INET
        self.client_socket = socket.socket(address_family, socket.SOCK_DGRAM)

    def send_message(self, message):
        # Sends a message to the server and waits for an acknowledgment
        self.sequence_number += 1
        formatted_message = f"{message}|ACK|{self.sequence_number}"
        # reads the ACK message formated like {message}|ACK|{sequence_number}
        retries = 0
        message_sent = False

        while retries < self.MAX_RETRIES:
        # while loop to send the message and wait for the ACK
            if not message_sent:
                # Send the message to the server once per timeout
                self.client_socket.sendto(formatted_message.encode(), (self.server_address, self.server_port))
                print(f"Sent message to {self.server_address}:{self.server_port}: {message} (Seq: {self.sequence_number})")
                self.sent_packets += 1
                message_sent = True

            # Set a timeout for receiving acknowledgment
            self.client_socket.settimeout(2)

            try:
                # Receive acknowledgment from the server
                ack_message, _ = self.client_socket.recvfrom(1024)

                self.received_packets += 1

                # Check if the acknowledgment has the correct sequence number
                ack_sequence_number = int(ack_message.decode().split('|')[-1])

                if ack_sequence_number == self.sequence_number:
                    # If the sequence number is correct, print the acknowledgment and break out of the loop
                    print(f"Received acknowledgment from {self.server_address}:{self.server_port}: {ack_message.decode()}")
                    break

                print(f"Ignored acknowledgment with incorrect or outdated sequence number: {ack_sequence_number}")

            except socket.timeout:
                # If the client times out, resend the message
                print(f"Timed out. Retrying ({retries + 1}/{self.MAX_RETRIES})...")
                retries += 1
                message_sent = False

    def display_packet_graph(self):
        # Display a graph of sent and received packets
        labels = ['Sent', 'Received']
        counts = [self.sent_packets, self.received_packets]
        plt.bar(labels, counts, color=['blue', 'green'])
        plt.xlabel('Packets')
        plt.ylabel('Count')
        plt.title('Sent and Received Packets')
        plt.show()

    def run(self):
        # Runs the client
        try:
            while True:
                # Get a message from the user and send it to the server
                message = input("Enter a message (or 'exit' to quit): ")
                if message.lower() == 'exit':
                    break
                self.send_message(message)
        except KeyboardInterrupt:
            print("\nCtrl+C received. Exiting gracefully.")
        finally:
            self.client_socket.close()
            self.display_packet_graph()  # Call the new function before exiting

if __name__ == '__main__':
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python client.py <server IP address> <server port>")
        sys.exit(1)

    server_address = sys.argv[1]
    server_port = int(sys.argv[2])

    # Checks if the user has entered a valid port and address
    try:
        if server_port < 0 or server_port > 65535:
            raise ValueError
    except ValueError:
        print("Invalid port number. Port must be between 0 and 65535.")
        sys.exit(1)
    
    try:
        if ':' in server_address:
            socket.inet_pton(socket.AF_INET6, server_address)
        else:
            socket.inet_pton(socket.AF_INET, server_address)
    except socket.error:
        print("Invalid IP address.")
        sys.exit(1)

    client = Client(server_address, server_port)
    client.initialize_client()
    client.run()
