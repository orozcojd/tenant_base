import sqlite3
from config.memcached import Memcached
from pymemcache.client import base
from config.create import all_data
from config.sqlitedb import SqliteDb

mcached = Memcached('localhost', 11212) # memcached connection

def init_db():
  ''' Initialize db - creates tables.
  '''

  db = SqliteDb()
  conn = db.db()
  cursor = conn.cursor()
  print('sqlite database connection established.')
  # cursor.execute(''' DROP TABLE kv_items''')
  cursor.execute('''CREATE TABLE IF NOT EXISTS kv_items(id INTEGER PRIMARY KEY, key key VARCHAR(50), value key VARCHAR(50))''')
  
  print('populating database with 1000 records if not already in db...')
  for item in all_data: # populate database with dummy data
    cursor.execute('''INSERT OR IGNORE INTO kv_items(id, key, value) VALUES(?,?,?)''',
                  (item['id'], item['key'], item['value']))
  conn.commit()
  conn.close()


def add_items(key, val):
  ''' Inserts key,val pair into sqlite and in memcached
  '''

  db = SqliteDb()
  conn = db.db()
  cursor = conn.cursor()
  cursor.execute('''INSERT INTO kv_items(key, value) VALUES(?,?)''', (key, val))
  conn.commit()
  conn.close()
  mcached.set_cached(key, val)

def get_items(key):
  ''' First checks memcached for query result, if not found
  queries sqlite db and returns result
  '''
  print('inside get')
  db = SqliteDb()
  try: 
    res = mcached.get_cached(key)
    print('response is cached!')
  except:
    res = None
    print('Error connecting to memcached server.')
  if res is None:
    print('inside actions get items')
    if key == 'all_items':
      print('insie getting all sqlite')
      # print('all items')
      res = db.sel_all()
      # print('inside select all')
      # print(res)
    else:
      query = '''SELECT * FROM kv_items WHERE key=?'''
      res = db.exec_query(query, key)
    try:
      if res:
        mcached.set_cached(key, res)
    except Exception as e:
      print(e)
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