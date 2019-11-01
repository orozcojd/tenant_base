from http.server import HTTPServer, BaseHTTPRequestHandler
from config.memcached import Memcached
import socketserver
import json
import actions
import os
import cgi
import json

class Handler(BaseHTTPRequestHandler):
  ''' A sublass of BaseHTTPRequestHandler that responds to
  client requests by serving requested files if found
  '''

  mcached = Memcached('localhost', 11211) # memcached connection

  def respond(self, status, content_type, f):
    ''' Sets response headers and sends file content
    to the client
    '''

    self.send_response(status)
    self.send_header('Content-type', content_type)
    self.send_header('Content-length', len(f))
    self.end_headers()
    self.wfile.write(f)
  
  
  def do_POST(self):
    ''' Handles all POST requests from client. Inserts into db and cache data structure
    if key not already found.
    '''
    
    str_val = self.rfile.read(int(self.headers['content-length']))
    data = json.loads(str_val)
    try:
      self.mcached.set_cached(data['key'], data['value'])
      self.respond(200, 'text/html', bytes('', 'utf-8'))
    except Exception as e:
      print(e)
      self.respond(403, 'text/html', bytes('', 'utf-8'))


  def do_GET(self):
    ''' Handles all GET requests made by the client
    '''

    if self.path == '/':
      index = "index.html"
      f = open(index).read()
      self.respond(200, 'text/html', bytes(f, "utf-8"))
    elif self.path == '/items':
      items = actions.get_items('all_items')
      self.respond(200, 'application/json; charset=utf-8', bytes(json.dumps(items), 'utf-8'))
    elif self.path.endswith('.css'):
      file = open(os.path.curdir + self.path).read()
      self.respond(200, 'text/css', bytes(file, 'utf-8'))
    else:
      self.respond(200, 'text/plain', bytes('', 'utf-8'))


  def do_DELETE(self):
    ''' Handles all DELETE requests made by client. Deletes 
    kv pair from db and cache data structure
    '''

    key = self.path.split('/')[2]
    print(key)
    res = actions.delete_items(key)
    print(res)
    if res:
      self.respond(200, 'text/html', bytes('', "utf-8"))
    else:
      self.respond(403, 'text/html', bytes('', "utf-8"))
    
class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
  pass