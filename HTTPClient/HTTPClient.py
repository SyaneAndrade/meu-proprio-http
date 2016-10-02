import socket


class HttpClient(object):
    """docstring for HttpClient."""
    HTTP_VERSION = "HTTP/1.1"

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def GET(self, arg):
            pass

    def POST(self, arg):
        pass

    def PUT(self, arg):
        pass

    def DELETE(self, arg):
        pass

    def UPDATE(self, arg):
        pass

    def getURI(self, path):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dest(self.host, self.port)
        print("Para sair use CTRL+X\n")
        msg = raw_input()
        while msg != '\x18':
            upd.sendto(msg, dest)
            msg = raw_input()
        udp.close()
