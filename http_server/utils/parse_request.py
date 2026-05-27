import json
from typing import Any


def parse_startline(startline_and_header_text: str) -> tuple[dict[str, str], list[str]]:
    split_lines = startline_and_header_text.split("\r\n")
    method, path, version = split_lines[0].split()
    return {"method": method, "path": path, "version": version}, split_lines[1:]


def parse_header_lines(header_lines: list[str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for line in header_lines:
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()
    return headers


def parse_body(body_bytes: bytes | None, headers: dict[str, str]) -> Any:
    if not body_bytes:
        return None

    content_type = headers.get("Content-Type", None)
    if content_type == "text/plain":
        return body_bytes.decode("utf-8")
    elif content_type == "application/json":
        return json.loads(body_bytes)
    raise NotImplementedError()
