from server import HTTPServer


def main():
    serv = HTTPServer("localhost", 8000)
    serv.start()


if __name__ == "__main__":
    main()
