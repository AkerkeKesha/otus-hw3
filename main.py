import socket


def handle_request(server_socket):
    client_connection, client_address = server_socket.accept()
    raw_request = client_connection.recv(1024)
    response = application(parse(raw_request), start_response)
    client_connection.sendall(response)
    client_connection.close()


def application(environ, start_response):
    status = "HTTP/1.1 200 OK"
    headers = [('Content-Type', 'text/plain')]
    return start_response(status, headers)


def parse(raw_request):
    d = {}
    request = bytes.decode(raw_request).split("\r\n")
    first_line = request[0].split(" ")

    if len(first_line) == 3:
        d['method'], d['resource'], d['version'] = first_line
    elif len(first_line) == 2:
        d['method'], d['version'] = first_line

    for pair in request[1:]:
        if pair == '':
            continue
        header, value = pair.split(": ")
        d[header.strip().lower()] = value.strip()
    return d


def start_response(status, headers, content=""):
    response = f"{status}"
    for key, val in headers:
        response += "\n" + f"{key}: {val}"
    response = response.strip() + '\r\n\r\n' + content
    return response.encode("utf8")


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9005))
    server_socket.listen()
    while True:
        handle_request(server_socket)


def register(urls):
    pass


def main():
    #register(urls)
    run()


if __name__ == "__main__":
    main()

