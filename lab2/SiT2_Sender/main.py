import socket
import ssl
import base64
import datetime

def send_email_via_smtp_ssl(host, port, username, password, recipient, subject, body):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    context = ssl.create_default_context()
    secure_sock = context.wrap_socket(sock, server_hostname=host)
    
    try:
        secure_sock.connect((host, port))
        
        # Получаем ответ от серваера
        recv_data = secure_sock.recv(1024).decode()
        print("Server response:", recv_data)
        
        # Отправляем команду для идентификации клиента
        secure_sock.send(b'HELO smtp.mail.ru\r\n')
        recv_data = secure_sock.recv(1024).decode()
        print("HELO response:", recv_data)
        
        # Авторизируемся
        secure_sock.send(b'AUTH LOGIN\r\n')
        recv_data = secure_sock.recv(1024).decode()
        print("AUTH LOGIN response:", recv_data)
        
        # Отправляем юзернейм в base64
        secure_sock.send(base64.b64encode(username.encode()) + b'\r\n')
        recv_data = secure_sock.recv(1024).decode()
        print("Username response:", recv_data)
        
        # Отправляем пароль в base64
        secure_sock.send(base64.b64encode(password.encode()) + b'\r\n')
        recv_data = secure_sock.recv(1024).decode()
        print("Password response:", recv_data)
        
        # Отправляем почту отправителя
        secure_sock.send(f"MAIL FROM:<{username}>\r\n".encode())
        recv_data = secure_sock.recv(1024).decode()
        print("MAIL FROM response:", recv_data)
        
        #  Отправляем почту получателя
        secure_sock.send(f"RCPT TO:<{recipient}>\r\n".encode())
        recv_data = secure_sock.recv(1024).decode()
        print("RCPT TO response:", recv_data)
        
        # Отправляем флаг DATA для дольнейшей отправки письма
        secure_sock.send(b'DATA\r\n')
        recv_data = secure_sock.recv(1024).decode()
        print("DATA response:", recv_data)
        
        # Строим письмо
        email_message = (
            f"Subject: {subject}\r\n"
            f"From: {username}\r\n"
            f"To: {recipient}\r\n"
            f"Date: {datetime.datetime.now()}\r\n"
            "\r\n"  # Разделяем заголовки от тела
            f"{body}\r\n"
            ".\r\n"  # Помечаем конец письма
        )
        
        #Отправляем сожержимое
        secure_sock.send(email_message.encode())
        recv_data = secure_sock.recv(1024).decode()
        print("Email sending response:", recv_data)
        
        # Приостанавливаем соединение
        secure_sock.send(b'QUIT\r\n')
        recv_data = secure_sock.recv(1024).decode()
        print("QUIT response:", recv_data)
        
    finally:
        secure_sock.close()

smtp_server_host = "smtp.mail.ru"
smtp_server_port = 465
smtp_username = "fsb3003pro@mail.ru"
smtp_password = "AS7rB0aDAxdSDAEtRrkj"
email_recipient = "fsb2004pro@gmail.com"
email_subject = input("Enter email subject: ")
email_body = input("Enter email body: ")

send_email_via_smtp_ssl(
    smtp_server_host, smtp_server_port, smtp_username, 
    smtp_password, email_recipient, email_subject, email_body
)