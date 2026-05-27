import socket

from http_server.request import Request
from http_server.response import HTTP404_NotFound_Response, HTTP405_MethodNotAllowed_Response
from http_server.utils.read_request import read_startline_and_header_text, read_body
from http_server.utils.parse_request import parse_startline, parse_header_lines, parse_body


class HTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.routes = {}

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen(128)

        while True:
            client, addr = self.server.accept()
            self.__handle_client(client, addr)
            client.close()
    
    def __register_method(self, method, path, callback):
        route = self.routes.get(path, None)
        
        if not route:
            self.routes[path] = {
                method: callback
            }
            return

        method_callback = route.get(method, None)

        if method_callback:
            raise ValueError("Can't register more than one callbacks for a path and method")
        
        route[method] = callback

    def get(self, path):
        def decorator(callback):
            self.__register_method("GET", path, callback)
            return callback
        return decorator
        
    def __handle_client(self, client, addr):
        # read and parse headers
        startline_and_header_text, leftover_bytes = read_startline_and_header_text(client)
        startline, header_lines = parse_startline(startline_and_header_text)
        headers = parse_header_lines(header_lines)

        # read and parse body
        body_bytes = read_body(client, leftover_bytes, headers)
        body = parse_body(body_bytes, headers)

        # build response
        request = Request(startline["method"], startline["path"], startline["version"], headers, body)
        response = self.__handle_request(request).build()

        client.send(response.encode("utf-8"))

    def __handle_request(self, request):
        route = self.routes.get(request.path, None)

        if not route:
            return HTTP404_NotFound_Response(f"{request.path} not found")
        
        method_callback = route.get(request.method, None)

        if not method_callback:
            return HTTP405_MethodNotAllowed_Response(f"{request.method} method not allowed")
        
        return method_callback(request)
