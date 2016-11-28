from HTTPServer.httpserver import *
import threading
import _thread

class HTTPServer_thread(HTTPServer):
    """docstring for HTTPServer_thread."""
    def __init__(self, host, port, tree):
        HTTPServer.__init__(self, host, port, tree)

    def iniciaServer(self):
        try:
            udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            orig = (self.host, self.port)
            udp.bind(orig)
            udp.listen(10)
            print('Serve HTTP na porta %s ...' % self.port)
            while True:
                client_connection, client_address = udp.accept()
                client_connection.settimeout(10)
                _thread.start_new_thread(HTTPServer.protocolHTTP,
                                         (self, client_connection))
                # t = threading.Thread(target=HTTPServer.protocolHTTP,
                #                      args=(self, client_connection))
                # t.start()

            udp.close()
        except:
            print("Conexão não estabelicida " + "\n")
            raise
