
from socketserver import StreamRequestHandler, ThreadingMixIn, TCPServer

class ThreadedTCPRequestHandler(StreamRequestHandler):
  ''' A sublass of StreamRequestHandler that responds to
  client requests by serving a subset of the memcache protocol. 
  '''

  cache = {} #caching data structure

  def get_line(self):
    ''' Returns a stripped readline of input stream
    '''

    return self.rfile.readline().strip()
  def respond(self, data):
    ''' Writes data to output stream
    '''

    self.wfile.write((data+'\r\n').encode('utf-8'))

  def get_key(self):
    ''' Parses arguments from input, gets value if key found in
    cache data structure
    '''

    res = b''
    keys = self.split_data[1:]
    # print(keys)
    for key in keys:
      retrieved = self.cache.get(key)
      if retrieved:
        flag, expiry, value = retrieved
        # VALUE <key> <flags> <bytes> [<cas unique>]\r\n
        # <data block>\r\n
        res += b'VALUE %s %d %d\r\n%s\r\n' % (key, flag, len(value), value)
    self.wfile.write(res + b'END\r\n') # add END to response, client expects

  def set_key(self):
    ''' Parses arguments from input, sets kv pair in cache data structure
    and writes output
    '''

    if len(self.split_data) < 5:
      self.respond('ERROR')
    else:
      args = self.split_data[1:5] 
      noreply = len(self.split_data) == 6 # last argument of set is noreply
      key, flag, expiry, byte_length = args # unpack required set args
      value = self.rfile.read(int(byte_length)+2) # +2 for \r char
      self.cache[key] = (int(flag), expiry, value[:-2]) # remove \r char
      if not noreply:
        self.respond('STORED')

  def del_key(self):
    ''' Parses arguments from input, del k,v pair from cache data structure
    if found, writes output appropriately
    '''

    if len(self.split_data) < 2:
      self.respond('ERROR')
    else:
      key = self.split_data[1]
      noreply = len(self.split_data) == 3 # if 3 arguments passed noreply is set
      if self.cache.pop(key, None):
        if not noreply:
            self.respond('DELETED')
      else:
        self.respond('NOT FOUND')
  def handle(self):
    ''' Main request handler function. Responds to input stream commands
    and reacts to set, get, delete commands appropriately
    '''

    while 1:
      if not self.rfile.peek():
        break
      data = self.get_line()
      if not data:
        self.respond('ERROR')
      else:
        self.split_data = data.split()
        self.command = self.split_data[0].lower()

        if self.command == b'set':
          self.set_key()
        elif self.command == b'get':
          self.get_key()
        elif self.command == b'delete':
          self.del_key()

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
  print('Threaded handler')
  pass