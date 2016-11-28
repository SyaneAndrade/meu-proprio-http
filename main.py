from HTTPServer.httpserver import *
from HTTPServer.httpserver_thread import *
from SA.Tree import *


if __name__ == '__main__':
    # Iniciando o diretorio raiz e o conteudo do arquivo
    snake = Tree('snake', 'rarararororoelatemehumaso')
    # Iniciando o server no localhost na porta 8888
    # se quiser outra porta é só editar aqui
    print("Escolha qual tipo de server você quer inicializar\n")
    print("Servidor com thread - (1)\n" + "Servidor sem thread(2)\n")
    a = input()
    if a == '1':
        server = HTTPServer_thread('localhost', 8888, snake)
        server.iniciaServer()
    elif a == '2':
        server = HTTPServer('localhost', 8888, snake)
        server.iniciaServer()
    else:
        print("Entrada invalida!")
