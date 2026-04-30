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
            client.close()

    def handle_client(self, client, addr):
        header_text, leftover_bytes = self.read_header(client)
        split_lines = header_text.split("\r\n")

        method, path, version = split_lines[0].split()
        print(method, path, version)

        headers = self.parse_header(split_lines[1:])
        print(headers)

    def read_header(self, client):
        buffer = b""
        delimeter = b"\r\n\r\n"

        while True:
            chunk = client.recv(1024)
            if not chunk:
                raise ConnectionError("The socket connection was closed.")

            buffer += chunk
            if delimeter in buffer:
                break

        header_bytes, _, leftover_bytes = buffer.partition(delimeter)
        header_text = header_bytes.decode("utf-8")
        return header_text, leftover_bytes

    def parse_header(self, split_lines):
        headers = {}
        for line in split_lines:
            key, value = line.split(": ", 1)
            headers[key] = value
        return headers

    def build_response(self):
        raise NotImplementedError()
