import socket
import threading
import pickle

HOST = 'localhost'
PORT = 12345
registered_calculators = {}

def register(message, addr):
    calculator_id = message['id']
    registered_calculators[calculator_id] = addr
    print(f"Registered calculator: {calculator_id} from {addr}")

def get_calculators(sock, addr):
    response = {
    'type': 'calculators_list',
    'calculators': registered_calculators
    }
    sock.sendto(pickle.dumps(response), addr)

def result(message):
    result = message['result']
    print(f"Received result from {message['id']}: {result}")

def handle_client(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data and addr:
                message = pickle.loads(data)
                
                match message['type']:
                    case 'register':
                        register(message, addr)
                    case 'get_calculators':
                        get_calculators(sock, addr)
                    case 'result':
                        result(message)
                    case _:
                        print("Error")
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        print(f"Server running on {HOST}:{PORT}")
        
        threading.Thread(target=handle_client, args=(sock,), daemon=True).start()
        input("Press Enter to stop the server...\n")

if __name__ == "__main__":
    main()
