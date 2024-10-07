from ftplib import FTP
import os

class FTPClient:
    def __init__(self, host, user='anonymous', passwd='', port=21):
        self.ftp = FTP()
        self.ftp.connect(host, port)
        self.ftp.login(user, passwd)
        print(f"Connected to {host}")

    def list_files(self):
        """List files and directories in the current directory."""
        files = self.ftp.nlst()
        for file in files:
            print(file)

    def get_file_size(self, filename):
        """Get the size of a file."""
        try:
            size = self.ftp.size(filename)
            print(f"Size of {filename}: {size} bytes")
            return size
        except Exception as e:
            print(f"Error: {e}")
            return None

    def change_directory(self, path):
        """Change to another directory."""
        try:
            self.ftp.cwd(path)
            print(f"Changed directory to: {path}")
        except Exception as e:
            print(f"Error: {e}")

    def download_file(self, filename, local_path=None):
        """Download a file from the FTP server."""
        if local_path is None:
            local_path = os.path.join(os.getcwd(), filename)
        
        with open(local_path, 'wb') as f:
            def callback(data):
                f.write(data)
            
            self.ftp.retrbinary(f"RETR {filename}", callback)
            print(f"Downloaded {filename} to {local_path}")

    def close(self):
        """Close the FTP connection."""
        self.ftp.quit()
        print("Connection closed.")


if __name__ == "__main__":
    ftp_client = FTPClient('ftp.gnu.org', 'anonymous', 'anonymous')

    print("Files and directories in the current directory:")
    ftp_client.list_files()

    ftp_client.get_file_size('CRYPTO.README')

    ftp_client.change_directory('/pub')
    
    ftp_client.list_files()

    ftp_client.download_file('CRYPTO.README')

    ftp_client.close()
