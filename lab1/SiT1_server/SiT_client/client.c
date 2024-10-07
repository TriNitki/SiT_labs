#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <ws2tcpip.h>  // For inet_pton

#pragma comment(lib, "ws2_32.lib")

#define SERVER_ADDRESS "127.0.0.1"
#define SERVER_PORT 5062
#define BUFFER_SIZE 4096

int main() {
    WSADATA wsaData;
    SOCKET sock;
    struct sockaddr_in server;
    char request[BUFFER_SIZE];
    char response[BUFFER_SIZE];
    int response_len;
    int result;

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        return 1;
    }

    // Create a socket
    sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) {
        return 1;
    }

    // Setup the server address structure
    server.sin_family = AF_INET;
    server.sin_port = htons(SERVER_PORT);

    // Convert IP address
    result = inet_pton(AF_INET, SERVER_ADDRESS, &server.sin_addr);
    if (result != 1) {
        return 1;
    }

    // Connect to the server
    if (connect(sock, (struct sockaddr*)&server, sizeof(server)) == SOCKET_ERROR) {
        return 1;
    }

    // Create the HTTP POST request
    const char* json_body = "{\"String\":\"value\", \"Length\": 5}";
    snprintf(request, sizeof(request),
        "POST /api HTTP/1.1\r\n"
        "Host: %s:%d\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %zu\r\n"
        "Connection: close\r\n"
        "\r\n"
        "%s",
        SERVER_ADDRESS, SERVER_PORT, strlen(json_body), json_body);

    // Send the request
    if (send(sock, request, strlen(request), 0) == SOCKET_ERROR) {
        return 1;
    }

    // Receive the response
    response_len = recv(sock, response, sizeof(response) - 1, 0);
    if (response_len == SOCKET_ERROR) {
        return 1;
    }

    // Null-terminate and print the response
    response[response_len] = '\0';
    printf("Response received:\n%s\n", response);

    // Clean up
    closesocket(sock);
    WSACleanup();

    return 0;
}
