from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import json
import actions
import os

class Handler(BaseHTTPRequestHandler):
    ''' A sublass of BaseHTTPRequestHandler that responds to
    client requests by serving requested files if found
    '''

    def respond(self, status, content_type, f):
        ''' Sets response headers and sends file content
        to the client
        '''

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Content-length', len(f))
        self.end_headers()
        self.wfile.write(f)

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

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    pass