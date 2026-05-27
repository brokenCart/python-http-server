from http_server.server import HTTPServer
from http_server.response import TextResponse

serv = HTTPServer("localhost", 8000)

@serv.get("/")
def hello(request):
    return TextResponse(200, body=b"Hello, World!")

serv.start()
