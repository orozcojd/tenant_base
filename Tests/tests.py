import sys
sys.path.append("..")

from main import app
import actions
import unittest

class TestRoutes(unittest.TestCase):
  def setUp(self):
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    app.config['WTF_CSRF_ENABLED'] = False
    # actions.init_db('items_db.db') # initialize db tables
    self.app = app.test_client()
  
  def test_index_template(self):
    '''ENDPOINT /
    METHOD: GET
    TEST: Verify tempalte rendered is index.html
    '''

  def test_index_status(self):
    '''ENDPOINT /
    METHOD: GET
    TEST: Verify response status code equals 200
    '''
    response = self.app.get('/', content_type='html/text')
    self.assertEqual(response.status_code, 200)

  def test_get_all_items_status(self):
    ''' ENDPOINT: /items
    METHOD: GET
    TEST: Verify response status code equals 200
    '''

    response = self.app.get('/items', content_type='html/text')
    self.assertEqual(response.status_code, 200)

  def test_get_all_items_type(self):
    ''' ENDPOINT: /items
    METHOD: GET
    TEST: Verify response type is equal to list
    '''

  def test_get_items_status(self):
    ''' ENDPOINT: /items/<key>/
    METHOD: GET
    TEST: Verify response status code equals 200
    '''

    response = self.app.get('/items', content_type='application/json')
    self.assertEqual(response.status_code, 200)

  def test_get_items_type(self):
    ''' ENDPOINT: /items/<key>/
    METHOD: GET
    TEST: Verify response type is equal to list
    '''
    response = self.app.get('/items', content_type='application/json')
    # self.assertEquals(response.json, list(success=True))
  
  def test_post_items_status(self):
    ''' ENDPOINT: /items/
    METHOD: POST
    TEST: Verify response status code equals 200
    '''

  def test_post_items(self):
    ''' ENDPOINT: /items/
    METHOD: POST
    TEST: Verify response equals expected
    '''

  def test_post_items_invalid(self):
    ''' ENDPOINT: /items/
    METHOD: POST
    TEST: Verify response equals expected upon invalid params
    '''

if __name__ == '__main__':
  unittest.main()