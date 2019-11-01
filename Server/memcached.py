
from socketserver import StreamRequestHandler, ThreadingMixIn, TCPServer
from config.sqlitedb import SqliteDb

class ThreadedTCPRequestHandler(StreamRequestHandler):
  ''' A sublass of StreamRequestHandler that responds to
  client requests by serving a subset of the memcache protocol. 
  '''

  cache = {} #caching data structure
  db = SqliteDb() # sqlite database instance

  def respond(self, data):
    ''' Writes data to output stream
    '''

    self.wfile.write((data+'\r\n').encode('utf-8'))


  def insert_db(self, k, v):
    ''' inserts k,v pair into sqlite database and pops the all_items
    key from the cache data structure for reset
    '''

    if k != b'all_items':
      self.db.exec_query('''INSERT OR IGNORE INTO kv_items(key, value) VALUES(?,?)''', (k.decode(), v.decode()))
      self.cache.pop(b'all_items', None)


  def remove_db(self, k):
    ''' Deletes row from database where key is param
    '''

    self.db.exec_query('''DELETE FROM kv_items WHERE key=?''', (k,))
    print('deleted from sqlite database')


  def get_key(self):
    ''' Parses arguments from input, gets value if key found in
    cache data structure
    '''

    res = b''
    keys = self.split_data[1:]
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

    if len(self.split_data) < 5: # should only accept min 5 args
      self.respond('ERROR')
    else:
      args = self.split_data[1:5] 
      noreply = len(self.split_data) == 6 # last argument of set is noreply
      key, flag, expiry, byte_length = args # unpack required set args
      value = self.rfile.read(int(byte_length)+2) # +2 for \r\n char
      self.cache[key] = (int(flag), expiry, value[:-2]) # remove \r\n char
      try: 
        self.insert_db(key, value[:-2])
      except Exception as e:
        print(e)
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
      self.remove_db(key.decode())
      noreply = len(self.split_data) == 3 # if 3 arguments passed noreply is set
      if self.cache.pop(key, None):
        self.cache.pop(b'all_items', None)
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
      data = self.rfile.readline().strip()
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