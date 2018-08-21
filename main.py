import socket


def handle_request(server_socket):
    client_connection, client_address = server_socket.accept()
    raw_request = client_connection.recv(1024)
    response = application(parse(raw_request), start_response)
    print(response)
    client_connection.sendall(response)
    client_connection.close()


def application(environ, start_response):
    status = "HTTP/1.1 200 OK"
    headers = [('Content-Type', 'text/plain')]
    return start_response(status, headers)


def start_response(status, headers, content=""):
    response = f"{status}"
    for key, val in headers:
        response += "\n" + f"{key}: {val}"
        response += "\n\n" + content
    return response.encode("utf8")


def parse(raw_request):
    pass


def server_forever():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9010))
    server_socket.listen()
    print(server_socket)
    while True:
        handle_request(server_socket)


def main():
    server_forever()


if __name__ == "__main__":
    main()

