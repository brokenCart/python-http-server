import socket
import json


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

        body = None
        content_length = int(headers.get("Content-Length", 0))
        if content_length:
            content_type = headers.get("Content-Type", None)
            body_bytes = self.read_body(client, leftover_bytes, content_length)
            print(content_type)

            body = self.parse_body(body_bytes, content_type)
            print(body)
        
        response = self.build_response({
            "version": version,
            "method": method,
            "path": path,
            "headers": headers,
            "body": body
        })
        client.send(response.encode("utf-8"))
        
        print()

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
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
        return headers

    def read_body(self, client, leftover_bytes, content_length):
        body_bytes = leftover_bytes
        while len(body_bytes) < content_length:
            chunk = client.recv(min(1024, content_length - len(body_bytes)))
            if not chunk:
                raise ConnectionError("The socket connection was closed.")

            body_bytes += chunk
        return body_bytes
    
    def parse_body(self, body_bytes, content_type):
        if content_type == "text/plain":
            return body_bytes.decode("utf-8")
        elif content_type == "application/json":
            return json.loads(body_bytes)
        raise NotImplementedError()

    def build_response(self, req):
        res_lines = []
        if req["path"] == "/" and req["method"] == "GET":
            res_lines.append(f"{req['version']} 200 OK")
            res_lines.append(f"Content-Type: text/plain")
            res_lines.append(f"Content-Length: 13")
            res_lines.append(f"\r\nHello, World!")
        else:
            res_lines.append(f"{req['version']} 404 Not Found")
            res_lines.append(f"Content-Type: application/json")
            body = json.dumps({"error": "Resource not found", "detail": f"{req['path']} does not exist"})
            res_lines.append(f"Content-Length: {len(body)}")
            res_lines.append("\r\n" + body)
        return "\r\n".join(res_lines)
