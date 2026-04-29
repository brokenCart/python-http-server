import socket


class HTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen(128)

        while True:
            client, addr = self.server.accept()
            self.handle_client(client, addr)

    def handle_client(self, client, addr):
        raise NotImplementedError()

    def parse_request(self):
        raise NotImplementedError()

    def build_response(self):
        raise NotImplementedError()
