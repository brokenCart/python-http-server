import json


def parse_startline(startline_and_header_text):
    split_lines = startline_and_header_text.split("\r\n")
    method, path, version = split_lines[0].split()
    return {"method": method, "path": path, "version": version}, split_lines[1:]


def parse_header_lines(header_lines):
    headers = {}
    for line in header_lines:
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()
    return headers


def parse_body(body_bytes, headers):
    if not body_bytes:
        return

    content_type = headers.get("Content-Type", None)
    if content_type == "text/plain":
        return body_bytes.decode("utf-8")
    elif content_type == "application/json":
        return json.loads(body_bytes)
    raise NotImplementedError()
