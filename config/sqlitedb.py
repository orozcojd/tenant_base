import sqlite3

class SqliteDb:

  def db(self):
    ''' Creates and returns database connection
    '''

    db = sqlite3.connect('database/items_db.db')
    db.row_factory = self.dict_factory
    return db
  def cursor(self, db):
    ''' Creates cursor object from database connecction and returns it
    '''
    
    db.row_factory = self.dict_factory
    cursor = db.cursor()
    return cursor
  
  def dict_factory(self, cursor, row):
    ''' Returns dictionary object for sqlite row_factory
    '''

    d = {}
    for indx, col in enumerate(cursor.description):
        d[col[0]] = row[indx]
    return d

  def sel_all(self):
    ''' Queries database for all data and returns result
    '''

    db = self.db()
    cursor = self.cursor(db)
    cursor.execute('''SELECT * FROM kv_items''')
    res = cursor.fetchall()
    return res
  
  def exec_query(self, query, key):
    ''' Executes query of given key and returns result
    '''
    
    db = self.db()
    cursor = self.cursor(db)
    cursor.execute(query, (key,))
    res = cursor.fetchall()
    db.commit()
    db.close()
    return res