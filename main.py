from HTTPServer.HTTPServer import *
from SA.Tree import *


if __name__ == '__main__':
    # Iniciando o diretorio raiz e o conteudo do arquivo
    snake = Tree('snake', 'rarararororoelatemehumaso')
    # Iniciando o server no localhost na porta 8888
    # se quiser outra porta é só editar aqui
    server = HTTPServer('localhost', 8888, snake)
    server.iniciaServer()
