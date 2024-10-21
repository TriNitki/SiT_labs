import socket
import struct

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5001

def main():
    # Создаем TCP/IP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Коннектимся к серверу
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to {SERVER_IP}:{SERVER_PORT}")
        
        message = input("Enter a message: ")
        
        if len(message) > 256:
            print("Message too long! It must be under 256 bytes.")
            return
        
        # Отправляем днину сообщения байтами
        msg_length = len(message)
        client_socket.sendall(struct.pack('!I', msg_length))
        
        # Отправляем сообщение
        client_socket.sendall(message.encode())
        
        # Получаем половину строки от сервера
        response = client_socket.recv(128) 
        print("Server response:", response.decode())

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
