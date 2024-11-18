import socket
import pickle
import hashlib
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 12345
TASK_DATA = [(0.0, 1.0, 1000), (0.0, 1.0, 1000), (0.0, 1.0, 1000), (0.0, 1.0, 1000), (0.0, 1.0, 1000)]  # Пример данных для расчета

def send_task(sock, calculator_addr, task, task_id):
    data = {
        'type': 'task',
        'task_id': task_id,
        'task': task,
        'hash': hashlib.md5(pickle.dumps(task)).hexdigest()
    }
    sock.sendto(pickle.dumps(data), calculator_addr)

def request_calculators(sock):
    request = {'type': 'get_calculators'}
    sock.sendto(pickle.dumps(request), (SERVER_HOST, SERVER_PORT))
    sock.settimeout(2)
    try:
        data, _ = sock.recvfrom(4096)
        response = pickle.loads(data)
        if response['type'] == 'calculators_list':
            return response['calculators']
    except socket.timeout:
        print("Failed to get response from server")
    return {}

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:        
        while True:
            registered_calculators = request_calculators(sock)
            if registered_calculators:
                for i, task in enumerate(TASK_DATA):
                    calculator_id, calculator_addr = list(registered_calculators.items())[i % len(registered_calculators)]
                    send_task(sock, calculator_addr, task, i)
                    print(f"Sent task {i} to {calculator_id}")
            else:
                print("No calculators available")
            
            time.sleep(10)

if __name__ == "__main__":
    main()
