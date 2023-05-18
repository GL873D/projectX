import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

# Configuration
C2_SERVER_HOST = ''  # Server IP address or hostname
C2_SERVER_PORT = 12345  # Server port number
AES_KEY = b'some_secret_key'  # AES encryption key
SALT = b'some_salt'  # Salt for key derivation
IV = b'some_initialization_vector'  # Initialization vector for CBC mode

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class C2Server:
    def __init__(self):
        self.server = None
        self.client_sockets = []
        self.cipher = None

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((C2_SERVER_HOST, C2_SERVER_PORT))
        self.server.listen(5)
        logging.info(f"C2 Server started on {C2_SERVER_HOST}:{C2_SERVER_PORT}")

        while True:
            client_socket, client_address = self.server.accept()
            self.client_sockets.append(client_socket)
            logging.info(f"New client connected: {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            while True:
                encrypted_data = client_socket.recv(1024)
                if not encrypted_data:
                    break
                decrypted_data = self.decrypt(encrypted_data)
                self.process_instruction(decrypted_data)
        except socket.error as e:
            logging.error(f"Socket error occurred while handling client: {e}")
        except ValueError as e:
            logging.error(f"Decryption error occurred while handling client: {e}")
        finally:
            client_socket.close()
            self.client_sockets.remove(client_socket)

    def process_instruction(self, instruction):
        # Implement your logic to interpret and handle instructions here
        logging.info(f"Received instruction: {instruction}")

    def send_response(self, client_socket, response):
        encrypted_response = self.encrypt(response)
        client_socket.send(encrypted_response)

    def broadcast_message(self, message):
        encrypted_message = self.encrypt(message)
        for client_socket in self.client_sockets:
            client_socket.send(encrypted_message)

    def stop(self):
        for client_socket in self.client_sockets:
            client_socket.close()

        self.server.close()
        logging.info("C2 Server stopped.")

    def encrypt(self, plaintext):
        cipher = self.get_cipher()
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return encrypted_data

    def decrypt(self, encrypted_data):
        cipher = self.get_cipher()
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        return decrypted_data

    def get_cipher(self):
        if self.cipher is None:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=SALT,
                iterations=100000,
                backend=default_backend()
            )
            key = kdf.derive(AES_KEY)
            self.cipher = Cipher(algorithms.AES(key), modes.CBC(IV), backend=default_backend())
        return self.cipher


def main():
    c2_server = C2Server()
    try:
        c2_server.start()
    except KeyboardInterrupt:
        c2_server.stop()


if __name__ == '__main__':
    main()
