from http_server.response import JSONResponse, TextResponse
from http_server.server import HTTPServer

serv = HTTPServer("localhost", 8000)


@serv.get("/")
def hello(request):
    return TextResponse(200, body=b"Hello, World!")


@serv.get("/json/")
def hello_json(request):
    return JSONResponse(
        200, body={"message": "Hello, World!", "username": "brokenCart"}
    )


serv.start()
