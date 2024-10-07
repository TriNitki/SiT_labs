import socket
import struct

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5001

def main():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to {SERVER_IP}:{SERVER_PORT}")
        
        # Input message from the user
        message = input("Enter a message: ")
        
        if len(message) > 256:
            print("Message too long! It must be under 256 bytes.")
            return
        
        # Send the length of the message (in network byte order)
        msg_length = len(message)
        client_socket.sendall(struct.pack('!I', msg_length))
        
        # Send the actual message
        client_socket.sendall(message.encode())
        
        # Receive the response from the server (half of the string)
        response = client_socket.recv(128)  # Expect half of the message
        print("Server response:", response.decode())

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    main()
