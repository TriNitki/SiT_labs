import socket
import threading

def calculate_integral(f, a, b, n):
    dx = (b - a) / n
    result = sum(f(a + i * dx) for i in range(1, n + 1)) * dx
    return result

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            a, b, n = map(float, data.decode().split())
            result = calculate_integral(lambda x: x**2, a, b, int(n))
            conn.sendall(str(result).encode())
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def run_tcp_server(host='localhost', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"TCP Server listening on {host}:{port}")
        
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

def handle_udp_discovery(host='0.0.0.0', port=5001):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((host, port))
        print(f"UDP discovery server listening on {host}:{port}")
        
        while True:
            data, addr = udp_socket.recvfrom(1024)
            if data.decode() == "DISCOVER":
                print(f"Discovery request received from {addr}")
                udp_socket.sendto(b"localhost:5000", addr)

if __name__ == "__main__":
    threading.Thread(target=run_tcp_server, args=('0.0.0.0', 5000)).start()
    threading.Thread(target=handle_udp_discovery, args=('0.0.0.0', 5001)).start()
