import sqlite3
from config.memcached import Memcached
from pymemcache.client import base
from config.create import all_data
from config.sqlitedb import SqliteDb

mcached = Memcached('localhost', 11211) # memcached connection

def init_db():
  ''' Initialize db - creates tables.
  '''

  db = sqlite3.connect('database/items_db.db')
  print('sqlite database connection established.')
  cursor = db.cursor()
  # cursor.execute(''' DROP TABLE kv_items''')
  cursor.execute('''CREATE TABLE IF NOT EXISTS kv_items(id INTEGER PRIMARY KEY, key key VARCHAR(50), value key VARCHAR(50))''')
  print('populating database with 1000 records...')

  for item in all_data: # populate database with dummy data
    add_items(item['key'], item['value'])
  db.commit()
  db.close()

def dict_factory(cursor, row):
  ''' Conversion of sqlite row to dict objects
  '''

  d = {}
  for indx, col in enumerate(cursor.description):
      d[col[0]] = row[indx]
  return d

def add_items(key, val):
  ''' Inserts key,val pair into sqlite and in memcached
  '''

  db = sqlite3.connect('database/items_db.db')
  cursor = db.cursor()
  cursor.execute('''INSERT INTO kv_items(key, value) VALUES(?,?)''', (key, val))
  db.commit()
  db.close()
  mcached.set_cached(key, val)


def get_items(key):
  ''' First checks memcached for query result, if not found
  queries sqlite db and returns result
  '''
  
  db = SqliteDb()
  try: 
    res = mcached.get_cached(key)
  except:
    res = None
    print('Error connecting to memcached server.')
  if res is None:
    if key == 'all_items':
      print('all items')
      res = db.sel_all()
      print(res)
    else:
      query = '''SELECT * FROM kv_items WHERE key=?'''
      res = db.exec_query(query, key)
    try:
      mcached.set_cached(key, res)
    except:
      print('Error retrieving data from db.')
  else:
    print('Query was cached, returning result.')
    res = res.decode()
  return res

def delete_items(key):
  ''' Deletes items by key from sqlite and memcached.
  '''

  try: 
    mcached.del_cached(key)
    db = SqliteDb()
    query = '''DELETE FROM kv_items WHERE key=?'''
    db.exec_query(query, key)
    print('Deletion successful from sqlite and memcached.')
  except Exception as e:
    print(e)
    print('Error occurred trying to delete from db or memcached.')