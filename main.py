import socket
import sys
import os


def handle_request(server_socket, urls):
    #TODO: html returned and never used
    client_connection, client_address = server_socket.accept()
    raw_request = client_connection.recv(1024)
    request = parse(raw_request)
    html = route(request, urls)
    response = application(request, start_response)
    client_connection.sendall(response)
    client_connection.close()


def route(request, urls):
    #TODO: view not callable
    view = match_view(request, urls)
    print(view)
    return view(request)


def match_view(request, urls):
    try:
        url = parse_url(request)
        return urls[url]
    except KeyError:
        return f"Wrong url: {url}".encode('utf8')


def parse_url(request):
    return request['resource'].split("?")[0]


def hello(request):
    template_path = "templates/hello.html"
    context = {"title": "Hello Page",
               "name": "World"}
    if request['method'] == "POST":
        context.update(request.get_args())
        return render(request, template_path, context)
    return render(request, template_path, context)


def render(request, template_path, template_args):
    directory = os.path.join(BASE_DIR, os.path.join(PROJECT_NAME, template_path))
    with open(f"{directory}", 'r') as template:
        content = template.read()
        for parameter, arg in template_args.items():
            content = content.replace("{ %s }" % parameter, arg)
        return content.encode("utf8")


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


def run(urls):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[1])
    server_socket.bind(('localhost', port))
    server_socket.listen()
    while True:
        handle_request(server_socket, urls)


def register(urls):
    dict_urls = {}
    for url, vu in urls:
        dict_urls[url] = vu
    return dict_urls


def main(urls):
    urls = register(urls)
    run(urls)


if __name__ == "__main__":

    BASE_DIR = os.getcwd()
    PROJECT_NAME = 'project'
    urls = [('/hello/', hello), ]
    main(urls)

