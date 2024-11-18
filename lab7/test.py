import socket

def send_socks4_request(proxy_host, proxy_port, target_host, target_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((proxy_host, proxy_port))
        
        request = b"\x04\x01"
        request += target_port.to_bytes(2, 'big')
        request += socket.inet_aton(socket.gethostbyname(target_host))
        request += b"\x00"
        
        sock.sendall(request)
        
        response = sock.recv(8)
        if response[1] != 0x5A:
            print("Failed to connect")
            return
        
        print("Connected through proxy")
        
        http_request = f"GET /ip HTTP/1.1\r\nHost: {target_host}\r\n\r\n"
        sock.sendall(http_request.encode())
        
        response_data = sock.recv(4096)
        print("Response:")
        print(response_data.decode())
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    proxy_host = "127.0.0.1"
    proxy_port = 1080
    target_host = input("Enter target host (default `httpbin.org`): ")
    target_port = input("Enter target port (default `80`): ")
    
    try:
        target_port = int(target_port)
    except ValueError:
        target_port = 80
    
    if len(target_host) == 0:
        target_host = 'httpbin.org'
    
    if target_port < 1 and target_port > 65536:
        target_host = 80

    send_socks4_request(proxy_host, proxy_port, target_host, target_port)
