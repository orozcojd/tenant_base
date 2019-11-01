from pymemcache.client import base

class Memcached:
  def __init__(self, uri, port):
    self.uri = uri
    self.port = port

  def conn(self):
    return base.Client((self.uri, self.port))

  def get_cached(self, key):
    return self.conn().get(key)

  def set_cached(self, key, val):
    self.conn().set(key, val)
  
  def del_cached(self, key):
    self.conn().delete(key)