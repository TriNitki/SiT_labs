import socket
import threading

def handle_client(client_socket):
    def forward(source, destination):
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)
    
    try:
        request = client_socket.recv(1024)
        
        if len(request) < 9:
            client_socket.close()
            return
        
        version, command = request[0], request[1]
        if version != 4 or command != 1:
            client_socket.close()
            return
        
        port = int.from_bytes(request[2:4], 'big') # Целевой порт
        ip = '.'.join(map(str, request[4:8])) # Целевой ip
        
        user_id_end = request.find(b'\x00', 8)
        if user_id_end == -1:
            client_socket.close()
            return

        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.connect((ip, port))
        
        client_socket.sendall(b"\x00\x5a" + request[2:8])
        
        threading.Thread(target=forward, args=(client_socket, target_socket)).start()
        forward(target_socket, client_socket)
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_proxy_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"SOCKS4 Proxy started ({host}:{port})")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_proxy_server("0.0.0.0", 1080)
