import socket

class FTPClient:
    def __init__(self, host, user='anonymous', passwd='anonymous', port=21):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_dir = '/'

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.send_command(f"USER {self.user}")
        self.send_command(f"PASS {self.passwd}")
        print(self._recv_response())
        print(self._recv_response())
        print(self._recv_response())

    def send_command(self, command):
        self.sock.sendall((command + '\r\n').encode())
        return self._recv_response()

    def _recv_response(self):
        response = b""
        while b"\r\n" not in response:
            response += self.sock.recv(4096)
        return response.decode()

    def get_list(self):
        pasv_response = self.send_command("PASV")
        pasv_info = self._parse_pasv_response(pasv_response)

        if pasv_info:
            data_socket = self._create_data_socket(pasv_info)
            if data_socket:
                # Send LIST command
                self.send_command(f"LIST {self.current_dir}")
                
                # Retrieve the data from the data socket
                file_list = b""
                while True:
                    data = data_socket.recv(4096)
                    if not data:
                        break
                    file_list += data
                
                self._recv_response()
                
                data_socket.close()
                return file_list.decode()

        return "Failed to retrieve list."

    def get_file_size(self, filename):
        command = f"SIZE {filename}"
        response = self.send_command(command)
        return response

    def change_directory(self, path):
        command = f"CWD {path}"
        response = self.send_command(command)
        if "250" in response:
            self.current_dir = path
        return response

    def download_file(self, filename, local_filename):
        # Enter passive mode for data transfer
        pasv_response = self.send_command("PASV")
        pasv_info = self._parse_pasv_response(pasv_response)

        if pasv_info:
            data_socket = self._create_data_socket(pasv_info)
            command = f"RETR {filename}"
            self.send_command(command)
            
            with open(local_filename, 'wb') as file:
                while True:
                    data = data_socket.recv(4096)
                    if not data:
                        break
                    file.write(data)
            data_socket.close()

            return f"{filename} downloaded successfully."

    def _parse_pasv_response(self, response):
        # Parse the PASV response to get the IP and port for the data connection
        try:
            start = response.find('(') + 1
            end = response.find(')')
            pasv_data = response[start:end].split(',')
            
            if len(pasv_data) != 6:
                print(f"Unexpected PASV response format: {response}")
                return None

            # Extract the IP address and port from the PASV response
            ip_address = '.'.join(pasv_data[:4])
            p1 = int(pasv_data[4])
            p2 = int(pasv_data[5])
            port = (p1 << 8) + p2  # Combine p1 and p2 to get the full port number

            return ip_address, port

        except Exception as e:
            print(f"Error parsing PASV response: {e}")
            return None

    def _create_data_socket(self, pasv_info):
        ip_address, port = pasv_info
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((ip_address, port))
        return data_socket

    def close(self):
        self.send_command("QUIT")
        self.sock.close()

if __name__ == "__main__":
    ftp_client = FTPClient('ftp.gnu.org')

    # print("Files and directories in the current directory:")
    ftp_client.connect()
    print(ftp_client.get_list())
    print(ftp_client.download_file('CRYPTO.README', 'CRYPTO.README'))
    # print(ftp_client.get_file_size('CRYPTO.README'))
    print(ftp_client.change_directory("/pub"))
    # print(ftp_client.get_list())
    

    ftp_client.close()
