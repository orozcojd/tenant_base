# from flask import Flask, render_template, request, Response
import actions
import json
from Server.handler import ThreadedHTTPServer, Handler
from Server.memcached import ThreadedTCPRequestHandler, ThreadedTCPServer
import socketserver
import threading
import time

actions.init_db() # initialize db tables
# app = Flask(__name__)

# @app.route('/')
# def index():
#   return render_template('index.html')

# @app.route('/items')
# def get_items():
#   items = actions.get_items('all_items')
#   return json.dumps(items)

# @app.route('/items/', methods=['POST'])
# def item():
#   try:
#     key = request.json['key']
#     val = request.json['value']
#     actions.add_items(key, val)
#     return Response(json.dumps({'message': 'Successfully added items.'}), 
#       status=201, 
#       mimetype="application/json")
#   except Exception as e:
#     print(e)
#     return Response(json.dumps({'Error': 'Error trying to add items'}), 
#     status=422, 
#     mimetype="application/json")
      

# @app.route('/items/<string:key>/', methods=['GET', 'DELETE'])
# def items(key):
#   if request.method == 'GET':
#     try:
#       items = actions.get_items(key)
#       return json.dumps(items)
#     except Exception as e:
#       print(e)
#       print('inside exception')
#       return Response(json.dumps({'Error': 'Error trying to get key'}), 
#         status=422, 
#         mimetype="application/json")

#   elif request.method == 'DELETE':
#     try:
#       print('inside deletion method')
#       actions.delete_items(key)
#       return Response(json.dumps({'message': 'Items successfully deleted.'}), 
#         status=201, 
#         mimetype="application/json")
#     except:
#         return Response(json.dumps({'Error': 'Error trying to delete items.'}), 
#         status=422, 
#         mimetype="application/json")
              
# @app.errorhandler(404)
# def page_not_found(error):
#   return '404 - Page not found'


def serve_on_port(port):
    server = ThreadedHTTPServer(("localhost",port), Handler)
    server.serve_forever()
    return server

if __name__ == '__main__':

  HOST = 'localhost'
  MEM_C_PORT = 11212
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
    
    while 1:
      time.sleep(1)
  except Exception as e:
    print(e)
    socket_server.server_close()

  # app.run(host='0.0.0.0', port=PORT, debug=True)