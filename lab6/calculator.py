import socket
import pickle
import hashlib
import threading
import random

SERVER_HOST = 'localhost'
SERVER_PORT = 12345

def right_rectangle_integral(a, b, n):
    h = (b - a) / n
    result = 0
    for i in range(n):
        x = a + i * h
        result += f(x)
    result *= h
    return result

def f(x):
    return x ** 2

def handle_calculator():
    calc_id = f'calculator-{random.randint(0, 10000)}'
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(pickle.dumps({'type': 'register', 'id': calc_id}), (SERVER_HOST, SERVER_PORT))
        
        while True:
            data, _ = sock.recvfrom(1024)
            if data:
                task = pickle.loads(data)
                if task['type'] == 'task':
                    received_hash = task['hash']
                    calculated_hash = hashlib.md5(pickle.dumps(task['task'])).hexdigest()
                    if received_hash == calculated_hash:
                        result = right_rectangle_integral(*task['task'])
                        response = {
                            'type': 'result',
                            'id': calc_id,
                            'result': result,
                            'task_id': task['task_id']
                        }
                        print(f"{calc_id} result: {result}")
                        sock.sendto(pickle.dumps(response), (SERVER_HOST, SERVER_PORT))
                    else:
                        print("Hash mismatch, possible data corruption")

def main():
    threading.Thread(target=handle_calculator, daemon=True).start()
    threading.Thread(target=handle_calculator, daemon=True).start()
    input("Press Enter to stop the server...\n")

if __name__ == "__main__":
    main()
