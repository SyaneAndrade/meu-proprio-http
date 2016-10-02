import socket
from SA.Tree import *


class HTTPServer(object):
    """docstring for HTTPServer."""
    def __init__(self, host, port, tree):
        self.host = host
        self.port = port
        self.tree = []
        self.tree.append(tree)

    def search_snake(self, name):
        for i in self.tree:
            if(i.name == name):
                return i
        return None

    def GET(self, a, client_connection):
        aux = a.split(" ")[1]
        try:
            father = aux.replace("/", "\n").split("\n")[1]
        except:
            father = ''
        try:
            name = aux.replace("/", "\n").split("\n")[2]
        except:
            name = ''
        if(father == ''):
            signal = self.tree[0]
            http_response = """\
            GET 200 OK

            \n""" + signal.printing()
        elif(self.search_snake(father) is not None and name != ''):
            snake = self.search_snake(father)
            signal = snake.search_snake(name)
            if signal is not None:
                http_response = """\
                GET 200 OK

                \n""" + signal.printing()
            else:
                http_response = """\
                GET 404 NOT FOUND

                \n"""
        elif(self.search_snake(father) is not None and name == ''):
            signal = self.search_snake(father)
            http_response = """\
            GET 200 OK
            \n""" + signal.printing()
        else:
            http_response = """\
            GET 404 NOT FOUND

            \n"""

        client_connection.sendall(str.encode(http_response))

    def POST(self, a, client_connection):
        aux = a.split(" ")[1]
        try:
            father = aux.replace("/", "\n").split("\n")[1]
        except:
            father = ''
        try:
            name = aux.replace("/", "\n").split("\n")[2]
        except:
            name = ''
        try:
            data = a.split("\n")[16]
        except:
            data = ''
        if(self.search_snake(father) is not None and name != ''):
            snake = self.search_snake(father)
            signal = snake.exist_snake(name)
            if signal:
                baby_snake = snake.snake_born(data, name)
                http_response = """\
                POST 200 OK

                \n""" + baby_snake.printing()

        elif(father != '' and name == ''):
            if(self.search_snake(father) is None):
                new_snake = Tree(father, data)
                http_response = """\
                POST 200 OK

                \n""" + new_snake.printing()
                self.tree.append(new_snake)
            else:
                http_response = """\
                POST 403 FORBIDDEN

                \n"""
        else:
            http_response = """\
            POST 403 FORBIDDEN

            \n"""

        client_connection.sendall(str.encode(http_response))

    def PUT(self, a, client_connection):
        aux = a.split(" ")[1]
        try:
            father = aux.replace("/", "\n").split("\n")[1]
        except:
            father = ''
        try:
            name = aux.replace("/", "\n").split("\n")[2]
        except:
            name = ''
        data = a.split("\n")[16]
        if(self.search_snake(father) is not None and name != ''):
            snake = search_snake(father)
            signal = snake.search_snake(name)
            if signal:
                signal.modificationTree(data)
                http_response = """\
                PUT 200 OK

                \n""" + signal.printing()
                print(http_response)
                client_connection.sendall(str.encode(http_response))
            if(father != '' and self.search_snake(father) is not None):
                snake = self.search_snake(father)
                snake.modificationTree(data)
                http_response = """\
                PUT 200 OK

                \n""" + snake.printing()
            else:
                http_response = """\
                PUT 404 NOT FOUND

                \n"""
                print(http_response)
            client_connection.sendall(str.encode(http_response))

    def HEAD(self, a, client_connection):
                http_response = """\
                HEAD 200 OK

                \n""" + a
                client_connection.sendall(str.encode(http_response))

    def DELETE(self, a, client_connection):
            aux = a.split(" ")[1]
            try:
                father = aux.replace("/", "\n").split("\n")[1]
            except:
                father = ''
            try:
                name = aux.replace("/", "\n").split("\n")[2]
            except:
                name = ''
            if(self.search_snake(father) and name != ''):
                snake = self.search_snake(father)
                signal = snake.search_snake(name)
                if (signal is not None):
                    snake.deleteTree(signal)
                    http_response = """\
                    DELETE 200 OK
                    SUCESS!!!!
                    \n"""

            elif(self.search_snake(father) is not None and name == ''):
                snake = self.search_snake(father)
                self.tree.remove(snake)
                http_response = """\
                DELETE 200 OK
                SUCESS!!!!
                \n"""

            else:
                http_response = """\
                DELETE 404 NOT FOUND

                \n"""
            client_connection.sendall(str.encode(http_response))

    def iniciaServer(self):
        try:
            udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            orig = (self.host, self.port)
            udp.bind(orig)
            udp.listen(1)
            print('Serve HTTP na porta %s ...' % self.port)
            while True:
                client_connection, client_address = udp.accept()
                request = client_connection.recv(1024)
                # bytes.decode(request)
                client_connection.sendall(request)
                a = bytes.decode(request)
                # print(a)
                give = a.split(' ')[0]

                if (give == 'GET'):
                    self.GET(a, client_connection)

                elif (give == 'POST'):
                    self.POST(a, client_connection)

                elif (give == 'PUT'):
                    self.PUT(a, client_connection)

                elif (give == 'HEAD'):
                    self.HEAD(a, client_connection)
                elif(give == 'DELETE'):
                    self.DELETE(a, client_connection)

                else:
                    client_connection.sendall(str.encode(give + '503 SERVICE UNAVAILIABLE'))
                client_connection.close()
        except:
            print("Conexão não estabelicida " + "\n")
            raise
