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

    def deleteTree(self, name):
        self.tree.remove(name)

    """
        Nessario para criar as resposta para o cliente com as devidas mensagens
        Criação dos Cabeçalho e se necessario body
    """
    def response_headers(self, client, tree, status, quest, name):
        # Verificando o status da mensagem
        if status == 200:
            http_response = 'HTTP/1.1 ' + quest + ' 200 OK\r\n'
        elif status == 404:
            http_response = 'HTTP/1.1 ' + quest + ' 404 NOT FOUND\r\n'
        elif status == 403:
            http_response = 'HTTP/1.1' + quest + '403 FORBIDDEN\r\n'
        elif status == 400:
            http_response = 'HTTP/1.1' + quest + '400 BAD REQUEST\r\n'
        # Se existir a pasta da informação solicitada ele retorna os dados
        # na pasta
        if(tree is not None):
            client.send(str.encode(http_response))
            content_type = "Content-Type: text/html\r\n\r\n"
            body = '<html><body><h1>' + str(tree.data) + '</h1></body></html>'
            content_lenght = "Content-Lenght: " + str(len(body)) + "\r\n"
            head = tree.printing() + content_lenght +\
                content_type
            client.send(str.encode(head))
            client.send(str.encode(body))
        elif(quest == 'HEAD'):
            if(name is not None):
                client.send(str.encode(http_response))
                text = quest + ' ' + 'localhost:8888/' + name + ' HTTP/1.1\n'
                client.send(str.encode(text))
                head = ('HOST: ' + '127.0.0.1' + '\n'\
                        + 'PORT: ' + str(self.port) + '\r\n')
                client.send(str.encode(head))
            else:
                client.send(str.encode(http_response))
        else:
            client.send(str.encode(http_response))

    """
        Função para acessar o caminho da informação
    """
    def cut_request(self, a):
        # Linha que pega o caminho
        aux = a.split(" ")[1]
        try:
            # Separo o caminho onde tem / coloco /n e pego a raiz
            father = aux.replace("/", "\n").split("\n")[1]
        except:
            father = ''
        """
            se o caminho for longo tipo snake/coral/anaconda
            ele pegar até o try dar errado
        """
        try:
            # aqui pego os nos até as folhas e ponho em uma lista
            name = aux.replace("/", "\n").split("\n")[2:]
        except:
            name = ['']
        try:
            # aqui pego os dados para ser inserido na requisição
            # se for necessario
            value_data = a.split("\n")[13:]
            data = ''
            for i in range(0, len(value_data)):
                data = data + "\n" + value_data[i]
        except:
            data = ''
        return father, name, data

    """
        GET – Recupera dados e metadados da raiz do sistema
    """
    def GET(self, a, client_connection):
        # recebendo as variaveis do caminho
        father, name, data = self.cut_request(a)
        quest = 'GET'
        #  Procurando as informações no sistema de arquivo, se existirem
        #  serão retornadas e enviadas.
        #  Se não retorna status de erro
        if(father == ''):
            signal = self.tree[0]
            self.response_headers(client_connection, signal, 200, quest, None)

        elif(self.search_snake(father) is not None and name != []):
            snake = self.search_snake(father)
            if snake is not None:
                signal = snake.search_snake(name[0])
                if signal is not None:
                    if(len(name) > 1):
                        for i in range(1, len(name)):
                            signal = signal.search_snake(name[i])
                        if signal is not None:
                            self.response_headers(client_connection, signal,
                                                  200, quest, None)
                        else:
                            self.response_headers(client_connection, None,
                                                  404, quest, None)
                    else:
                        self.response_headers(client_connection, signal, 200,
                                              quest, None)
                else:
                    self.response_headers(client_connection, None, 404, quest,
                                          None)
            else:
                self.response_headers(client_connection, None, 404, quest,
                                      None)
        elif(father != '' and name == []):
            signal = self.search_snake(father)
            if signal is not None:
                self.response_headers(client_connection, signal, 200, quest,
                                      None)
            else:
                self.response_headers(client_connection, None, 404, quest,
                                      None)

        else:
            self.response_headers(client_connection, None, 404, quest, None)

    # POST – Cria arquivo com dados passados no corpo, se não
    # existe. Se já existe, retorna erro. Dados no corpo.
    def POST(self, a, client_connection):
        father, name, data = self.cut_request(a)
        quest = 'POST'
        # verificando o sistema
        # Se caso a raiz existir e o resto do caminho nao for vazio
        # ele procura até achar de quem será a subpasta
        if(self.search_snake(father) is not None and name != []):
            snake = self.search_snake(father)
            if snake is not None:
                if snake.exist_snake(name[0]) is not True:
                    snake_branch = snake.search_snake(name[0])
                    for i in range(1, len(name)-1):
                        snake_branch = snake_branch.search_snake(name[i])
                    if snake_branch is not None:
                        signal = snake_branch.exist_snake(name[len(name)-1])
                        # Se caso a subpasta no caminho indicado nao existir
                        # ele cria, se nao retorna erro.
                        if signal:
                            baby_snake = snake_branch.snake_born(data, name[len(name)-1])
                            self.response_headers(client_connection,
                                                  baby_snake, 200, quest, None)
                        else:
                            self.response_headers(client_connection, None, 403,
                                                  quest, None)
                    else:
                        self.response_headers(client_connection, None, 403,
                                              quest, None)
                else:
                    baby_snake = snake.snake_born(data, name[0])
                    self.response_headers(client_connection,
                                          baby_snake, 200, quest, None)
            # Se caso é pra criar um novo diretorio na raiz ele verifica se
            # ja existe,se nao existir ele cria o arquivo com os parametros,
            # se nao retorna erro
            else:
                self.response_headers(client_connection, None, 404, quest)
        elif(father != '' and name == []):
            snake = self.search_snake(father)
            if(self.search_snake(father) is None):
                new_snake = Tree(father, data)
                self.tree.append(new_snake)
                self.response_headers(client_connection, new_snake, 200, quest,
                                      None)
            else:
                self.response_headers(client_connection, None, 403, quest,
                                      None)
        else:
            self.response_headers(client_connection, None, 404, quest, None)

    # PUT – Modifica dados e metadados do arquivo, se já existe.
    # Se não existe, retorna erro. Dados no corpo.
    def PUT(self, a, client_connection):
        father, name, data = self.cut_request(a)
        quest = 'PUT'
        if(self.search_snake(father) is not None and name != []):
            snake = self.search_snake(father)
            aux = snake
            i = 0
            signal = None
            while (i < len(name)):
                if(name[i] != ''):
                    aux = aux.search_snake(name[i])
                    signal = aux
                i += 1
            if signal:
                signal.modificationTree(data)
                self.response_headers(client_connection, signal, 200,
                                      quest, None)
            else:
                self.response_headers(client_connection, None, 404, quest, None)
        elif(self.search_snake(father)is not None and name == []):
            snake = self.search_snake(father)
            snake.modificationTree(data)
            self.response_headers(client_connection, snake, 200, quest, None)
        else:
            self.response_headers(client_connection, None, 404, quest, None)

    """
        HEAD – Recupere apenas metadados do arquivo indicado.
    """
    def HEAD(self, a, client_connection):
        father, name, data = self.cut_request(a)
        quest = 'HEAD'
        if (father != '' and name != []):
            snake = self.search_snake(father)
            aux = snake
            i = 0
            signal = None
            while (i < len(name)):
                if(name[i] != ''):
                    aux = aux.search_snake(name[i])
                    signal = aux
                i += 1
            if signal:
                # nome = '' + father
                # for i in range(0, len(name)):
                #     nome = nome + '/'+name[i]
                self.response_headers(client_connection, signal, 200, quest,
                                      None)
            else:
                self.response_headers(client_connection, None, 400, quest,
                                      None)
        elif(father != '' and name == []):
            snake = self.search_snake(father)
            if snake is not None:
                self.response_headers(client_connection, snake, 200, quest,
                                      None)
            else:
                self.response_headers(client_connection, None, 400, quest,
                                      None)
        else:
            self.response_headers(client_connection, None, 400, quest,
                                  None)

    """
        DELETE – Remove arquivo se existe. Se não existe, retorna
        erro.
    """
    def DELETE(self, a, client_connection):
        father, name, data = self.cut_request(a)
        quest = 'DELETE'
        if(self.search_snake(father) and name != []):
            snake = self.search_snake(father)
            signal = snake.search_snake(name[0])
            i=1
            while (i < len(name)):
                if(name[i] != ''):
                    snake = signal
                    signal = signal.search_snake(name[i])
                i += 1
            if signal is not None:
                snake.deleteTree(signal)
                self.response_headers(client_connection, None, 200, quest,
                                      None)
            else:
                self.response_headers(client_connection, None, 400, quest,
                                      None)
        elif(self.search_snake(father) and name == []):
            snake = self.search_snake(father)
            self.deleteTree(snake)
            self.response_headers(client_connection, None, 200, quest,
                                  None)
        else:
            self.response_headers(client_connection, None, 400, quest,
                                  None)

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
                a = bytes.decode(request)
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
                    client_connection.sendall(str.encode('HTTP/1.1 ' + give + ' 503 SERVICE UNAVAILIABLE\r\n\r\n'))
                client_connection.close()
        except:
            print("Conexão não estabelicida " + "\n")
            raise
