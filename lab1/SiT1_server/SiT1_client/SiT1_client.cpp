#include <iostream>
#include <string>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "Ws2_32.lib")

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 5001

int main() {
    printf("Client C++\n");
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);

    // Создаем сокет
    SOCKET clientSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (clientSocket == INVALID_SOCKET) {
        std::cerr << "Socket creation failed" << std::endl;
        WSACleanup();
        return -1;
    }

    // Конфигурируем адрес сервера
    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    inet_pton(AF_INET, SERVER_IP, &serverAddr.sin_addr);
    serverAddr.sin_port = htons(SERVER_PORT);

    // Подключаемся к серверу
    if (connect(clientSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "Connection failed" << std::endl;
        closesocket(clientSocket);
        WSACleanup();
        return -1;
    }

    std::string message;
    std::cout << "Enter a message: ";
    std::getline(std::cin, message);

    if (message.length() > 256) {
        std::cerr << "Message too long!" << std::endl;
        closesocket(clientSocket);
        WSACleanup();
        return -1;
    }

    int msgLength = htonl(message.length());

    // Отправляем длину строки
    send(clientSocket, (char*)&msgLength, sizeof(msgLength), 0);

    // Отправляем строку
    send(clientSocket, message.c_str(), message.length(), 0);

    // Получаем ответ
    char buffer[128];
    int received = recv(clientSocket, buffer, sizeof(buffer), 0);
    if (received > 0) {
        buffer[received] = '\0';
        std::cout << "Server response: " << buffer << std::endl;
    }

    closesocket(clientSocket);
    WSACleanup();

    getchar();

    return 0;
}
