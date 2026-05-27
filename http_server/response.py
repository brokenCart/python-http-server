import json
from typing import Any

from http_server.utils.http_status_codes import HTTP_STATUS_CODES


class Response:
    status_code: int
    version: str
    headers: dict[str, str]
    body: Any

    def __init__(
        self,
        status_code: int,
        version: str = "HTTP/1.1",
        headers: dict[str, str] = {},
        body: Any = None,
    ) -> None:
        self.status_code = status_code
        self.version = version
        self.headers = headers
        self.body = body

    def set_header(self, key: str, value: str) -> None:
        self.headers[key.strip()] = value.strip()

    def build(self) -> str:
        delimeter = "\r\n"
        response_string = (
            f"{self.version} {self.status_code} {HTTP_STATUS_CODES[self.status_code]}"
            + delimeter
        )
        response_string += (
            delimeter.join([f"{key}: {self.headers[key]}" for key in self.headers])
            + delimeter
        )
        body_string = self.to_string(self.body)
        response_string += f"Content-Length: {len(body_string)}" + delimeter
        response_string += delimeter + body_string
        return response_string

    def to_string(self, b: Any) -> str:
        raise NotImplementedError()


class TextResponse(Response):
    def __init__(
        self,
        status_code: int,
        version: str = "HTTP/1.1",
        headers: dict[str, str] = {},
        body: bytes | None = None,
    ) -> None:
        super().__init__(status_code, version, headers, body)
        self.set_header("Content-Type", "text/plain")

    def to_string(self, b: bytes | str) -> str:
        if type(b) == str:
            return b
        return b.decode("utf-8")


class JSONResponse(Response):
    def __init__(
        self,
        status_code: int,
        version: str = "HTTP/1.1",
        headers: dict[str, str] = {},
        body: Any = None,
    ) -> None:
        super().__init__(status_code, version, headers, body)
        self.set_header("Content-Type", "application/json")

    def to_string(self, b: Any) -> str:
        return json.dumps(b)


class HTTP404_NotFound_Response(JSONResponse):
    def __init__(self, message: str) -> None:
        super().__init__(404, body={"error": "404 Not Found", "message": message})


class HTTP405_MethodNotAllowed_Response(JSONResponse):
    def __init__(self, message: str) -> None:
        super().__init__(
            405, body={"error": "405 Method Not Allowed", "message": message}
        )
