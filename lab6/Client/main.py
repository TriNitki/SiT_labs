import socket

def send_task_to_server(host='localhost', port=5000, a=0, b=1, n=1000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        task_data = f"{a} {b} {n}"
        client_socket.sendall(task_data.encode())
        
        result = client_socket.recv(1024).decode()
        print(f"Received result: {result}")

if __name__ == "__main__":
    send_task_to_server(a=0, b=1, n=10000)