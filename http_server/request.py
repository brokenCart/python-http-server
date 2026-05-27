from typing import Any


class Request:
    method: str
    path: str
    version: str
    headers: dict[str, str]
    body: Any

    def __init__(
        self,
        method: str,
        path: str,
        version: str,
        headers: dict[str, str],
        body: Any,
    ) -> None:
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.body = body
