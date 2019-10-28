from flask import Flask, render_template, request, Response
import actions
import json

PORT = 8000

actions.init_db() # initialize db tables


app = Flask(__name__)

@app.route('/')
def index():
      return render_template('index.html')

@app.route('/items')
def get_items():
      items = actions.get_items('all_items')
      return json.dumps(items)

@app.route('/items/', methods=['POST'])
def item():
      try:
            key = request.json['key']
            val = request.json['value']
            actions.add_items(key, val)
            return Response(json.dumps({'message': 'Successfully added items.'}), 
                  status=201, 
                  mimetype="application/json")
      except Exception as e:
            print(e)
            return Response(json.dumps({'Error': 'Error trying to add items'}), 
            status=422, 
            mimetype="application/json")
      

@app.route('/items/<string:key>/', methods=['GET', 'DELETE'])
def items(key):
      if request.method == 'GET':
            try:
                  items = actions.get_items(key)
                  return json.dumps(items)
            except Exception as e:
                  print(e)
                  print('inside exception')
                  return Response(json.dumps({'Error': 'Error trying to get key'}), 
                  status=422, 
                  mimetype="application/json")

      elif request.method == 'DELETE':
            try:
                  print('inside deletion method')
                  actions.delete_items(key)
                  return Response(json.dumps({'message': 'Items successfully deleted.'}), 
                  status=201, 
                  mimetype="application/json")
            except:
                  return Response(json.dumps({'Error': 'Error trying to delete items.'}), 
                  status=422, 
                  mimetype="application/json")
            
      
@app.errorhandler(404)
def page_not_found(error):
      return '404 - Page not found'


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=PORT, debug=True)