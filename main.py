import actions
from Server.handler import ThreadedHTTPServer, Handler
from Server.memcached import ThreadedTCPRequestHandler, ThreadedTCPServer
import socketserver
import threading
import time


def serve_on_port(port):
  ''' Creates instance of HTTPServer class and creates connection
  '''

  server = ThreadedHTTPServer(("localhost",port), Handler)
  server.serve_forever()
  return server

if __name__ == '__main__':

  HOST = 'localhost'
  MEM_C_PORT = 11211
  HTTP_SERVER_PORT = 8000

  # HTTP Server
  server = serve_on_port
  threading.Thread(target=server, args=[HTTP_SERVER_PORT]).start()

  try:
    # Memcache socketserver
    socket_server = ThreadedTCPServer((HOST, MEM_C_PORT), ThreadedTCPRequestHandler)
    server_thread_a = threading.Thread(target=socket_server.serve_forever)
    server_thread_a.setDaemon(True)
    server_thread_a.start()

    actions.init_db() # initialize db tables
    while 1:
      try:
        time.sleep(1)
      except:
        exit()
  except:
    socket_server.server_close()
