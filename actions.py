import sqlite3
import os
from config.memcached import Memcached
from pymemcache.client import base
from config.create import all_data
from config.sqlitedb import SqliteDb

mcached = Memcached('localhost', 11211) # memcached connection

def init_db():
  ''' Initialize db - creates tables.
  '''

  db = SqliteDb()
  print('sqlite database connection established.')
  db.exec_query('''CREATE TABLE IF NOT EXISTS kv_items(id INTEGER PRIMARY KEY, key VARCHAR(50) UNIQUE, value VARCHAR(50))''')
  res = db.sel_all()

  if not res:
    print('populating database with 484 unique records...')
    for item in all_data: # populate database with dummy data
      mcached.set_cached(item['key'], item['value'])
  else:
    print('populating memcache from existing database...')
    for item in res:
      mcached.set_cached(item['key'], item['value'])
  print('Database and cache set.')


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
    print('inside actions get items')
    res = db.sel_all()
    try:
      if res:
        mcached.set_cached(key, res)
    except Exception as e:
      print(e)
      print('Error retrieving data from db.')
  else:
    res = res.decode()
    # print(res)
    print('Query was cached, returning result.')
  return res

def delete_items(key):
    ''' Deletes items by key from sqlite and memcached.
    '''

    try: 
      mcached.del_cached(key)
      db = SqliteDb()
      query = '''DELETE FROM kv_items WHERE key=?'''
      print(key)
      db.exec_query(query, (key,))
      print('Deletion successful from sqlite and memcached.')
      return True
    except Exception as e:
      print(e)
      print('Error occurred trying to delete from db or memcached.')
      return False