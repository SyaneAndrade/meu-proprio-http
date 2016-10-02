from HTTPServer.HTTPServer import *
from SA.Tree import *


if __name__ == '__main__':
    snake = Tree('snake', 'rarararororoelatemehumaso')
    server = HTTPServer('localhost', 8888, snake)
    server.iniciaServer()
