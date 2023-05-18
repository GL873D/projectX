import socket
import threading

C2_SERVER_HOST = ''  # Server IP address or hostname
C2_SERVER_PORT = 12345  # Server port number

class C2Server:
    def __init__(self):
        self.server = None
        self.client_sockets = []

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((C2_SERVER_HOST, C2_SERVER_PORT))
        self.server.listen(5)
        print(f"C2 Server started on {C2_SERVER_HOST}:{C2_SERVER_PORT}")

        while True:
            client_socket, client_address = self.server.accept()
            self.client_sockets.append(client_socket)
            print(f"New client connected: {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                self.process_instruction(data)
        except Exception as e:
            print(f"Error handling client: {e}")

        client_socket.close()
        self.client_sockets.remove(client_socket)

    def process_instruction(self, instruction):
        # Implement your logic to interpret and handle instructions here
        print(f"Received instruction: {instruction}")

    def send_response(self, client_socket, response):
        client_socket.send(response.encode())

    def broadcast_message(self, message):
        for client_socket in self.client_sockets:
            self.send_response(client_socket, message)

    def stop(self):
        for client_socket in self.client_sockets:
            client_socket.close()

        self.server.close()
        print("C2 Server stopped.")


def main():
    c2_server = C2Server()
    try:
        c2_server.start()
    except KeyboardInterrupt:
        c2_server.stop()


if __name__ == '__main__':
    main()
