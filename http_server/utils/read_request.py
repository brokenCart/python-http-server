import socket


def read_startline_and_header_text(client: socket.socket) -> tuple[str, bytes]:
    buffer = b""
    delimeter = b"\r\n\r\n"

    while True:
        chunk = client.recv(1024)
        if not chunk:
            raise ConnectionError("The socket connection was closed.")

        buffer += chunk
        if delimeter in buffer:
            break

    header_bytes, leftover_bytes = buffer.split(delimeter)
    header_text = header_bytes.decode("utf-8")
    return header_text, leftover_bytes


def read_body(
    client: socket.socket, leftover_bytes: bytes, headers: dict[str, str]
) -> bytes | None:
    content_type = headers.get("Content-Type", None)
    content_length = int(headers.get("Content-Length", 0))

    both = all([content_type, content_length])
    atleast_one = any([content_type, content_length])
    if not both and atleast_one:
        raise ValueError(
            "Bad Request: Both Content-Type and Content-Length headers are required to read body"
        )

    if not both and not atleast_one:
        return None

    body_bytes = leftover_bytes
    while len(body_bytes) < content_length:
        chunk = client.recv(min(1024, content_length - len(body_bytes)))
        if not chunk:
            raise ConnectionError("The socket connection was closed.")

        body_bytes += chunk
    return body_bytes
