import socket


def server_forever():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9005))
    server_socket.listen()
    print(server_socket)
    while True:
        client_connection, client_address = server_socket.accept()
        request = client_connection.recv(1024)
        print("Request: ", request)

        client_connection.sendall(b"HTTP/1.1 200 OK\n\nHello!")
        client_connection.close()


def main():
    server_forever()


if __name__ == "__main__":
    main()

