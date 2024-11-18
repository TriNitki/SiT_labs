import socket

def discover_server(port=5001):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.sendto(b"DISCOVER", ('<broadcast>', port))
        udp_socket.settimeout(5)
        try:
            response, addr = udp_socket.recvfrom(1024)
            return response.decode(), addr
        except socket.timeout:
            print("No server discovered")
            return None

if __name__ == "__main__":
    response, server_addr = discover_server()
    if server_addr and response:
        print(f"Server found: {server_addr[0]}:{server_addr[1]}\nServer response: {response}")
