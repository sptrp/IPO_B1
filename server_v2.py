""" 
B2 websocket server
"""

# TODO: 
# pip install flask
# pip install flask_cors (to get rid of cors https://stackoverflow.com/questions/20035101/why-does-my-javascript-code-receive-a-no-access-control-allow-origin-header-i)
# pip install pandas
# pip install flask_restx (for automatic documentation etc.)
# pip install xmltodict
# pip install lxml
# pip install configupdater
# pip install xmlschema


from http.server import (HTTPServer, BaseHTTPRequestHandler)
import functools
from flask import (Flask, json, request, jsonify, Blueprint, render_template, session)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restx import (Api, Resource, fields)

import pandas as pd  
import lxml.etree as et
import os
import sys
import helper_v2 as helper
import logging 

from json import dumps

# logger
# logging.basicConfig(level=logging.DEBUG)

xml = os.path.join(sys.path[0], 'data/kurse.xml')  #Quelle: https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
schema = os.path.join(sys.path[0], 'data/kurse.xsd')         #Damit es unter Linux, Windows und Mac laeuft
ClientXml = os.path.join(sys.path[0], 'data/kunden.xml')
ClientSchema = os.path.join(sys.path[0], 'data/kunden.xsd')
request_schema = os.path.join(sys.path[0], 'data/request.xsd')  

# server
app = Flask(__name__)
# use blueprints to avoid CORS errors (Nikolai's advice)
bp = Blueprint('api', __name__, url_prefix='/api/')
api = Api(bp)
app.register_blueprint(bp)
app.secret_key = 'some secret key'

# parse client and return json with concrete client
def find_client(request):
  rows = []
  tree = et.parse(ClientXml)
  root = tree.getroot()

  for key, value in request.items():
    if key == 'id':
      path = helper.path_constructor_parentnode(value)

  try:
    # parse all (should be 1) found elements
    for targ in root.xpath(path): # https://stackoverflow.com/questions/21746525/get-all-parents-of-xml-node-using-python
      #for dept in targ.xpath('ancestor-or-self::kunde'):
        rows.append({ 
                      'id':targ.find('id').text,
                      'username':targ.find('username').text,
                      'firstname':targ.find('vorname').text,
                      'lastname': targ.find('nachname').text,
                      'adress': {
                        'street': targ.find('adresse/strasse').text,
                        'zipcode': targ.find('adresse/plz').text,
                        'city': targ.find('adresse/ort').text,
                        'country': targ.find('adresse/land').text },
                      'mail': targ.find('mail').text,
                    })
  except IOError:
    print("I/O error")
                                                                           
  print(rows)
  return rows

# parse course and return json
def find_all_courses():
  tree = et.parse(xml)
  root = tree.getroot()
  rows = []
  
  try:
    # parse elements and write to json
    for dept in root:
      keywords = ""
      for kw in dept.findall('schlagwort'):
          keywords = keywords + kw.text + " "

      rows.append({ 'guid':dept.find('guid').text, 'number': dept.find('nummer').text, 
                    'name': dept.find('name').text, 'subtitle': dept.find('untertitel').text,
                    'category': dept.find('dvv_kategorie').text, 'min_members': dept.find('minimale_teilnehmerzahl').text,
                    'max_members': dept.find('maximale_teilnehmerzahl').text, 'appointments': dept.find('anzahl_termine').text,
                    'begin_date': dept.find('beginn_datum').text, 'end_date': dept.find('ende_datum').text,
                    'target_audience': dept.find('zielgruppe').text, 'keywords': keywords,
                    'location': { 'name': dept.find('veranstaltungsort/name').text, 'country': dept.find('veranstaltungsort/adresse/land').text, 
                    'zipcode': dept.find('veranstaltungsort/adresse/plz').text, 'region': dept.find('veranstaltungsort/adresse/ort').text, 
                    'street': dept.find('veranstaltungsort/adresse/strasse').text, 'barrier_free': dept.find('veranstaltungsort/barrierefrei').text },
                    'price': { 'amount': dept.find('preis/betrag').text, 'discount_possible': dept.find('preis/rabatt_moeglich').text, 'price_reduced': dept.find('preis/zusatz').text },
                    'web': { 'type': dept.find('webadresse/typ').text, 'name': 'webadresse/name', 'uri': dept.find('webadresse/uri').text }
                    })

  except IOError:
    print("I/O error")
  
  return rows

# parse course and return json with concrete course
def find_course(request):
  rows = []
  search_elem = None
  search_value = None
  tree = et.parse(xml)
  root = tree.getroot()
  search_key = None

  # search element and value from request  
  for key, value in request.items():
    if value != None:
      # build path for query
      if key == 'diverse':
        # TODO: bug, finds entry two times
        path = helper.path_constructor_divers(value)
      else:
        search_key = key
        search_key = 'nummer' if (key == 'number') else search_key
        search_key = 'untertitel' if (key == 'subtitle') else search_key
        search_key = 'schlagwort' if (key == 'keywords') else search_key  
        path = helper.path_constructor_elem(search_key, value)

  try:
    # parse all found elements
    for targ in root.xpath(path): # https://stackoverflow.com/questions/21746525/get-all-parents-of-xml-node-using-python
      for dept in targ.xpath('ancestor-or-self::veranstaltung'):
        keywords = ""
        # combine all Schlagwoerter to one text
        for kw in dept.findall('schlagwort'):
          keywords = keywords + kw.text + " "

        rows.append({ 'guid':dept.find('guid').text, 'number': dept.find('nummer').text, 
                      'name': dept.find('name').text, 'subtitle': dept.find('untertitel').text,
                      'category': dept.find('dvv_kategorie').text, 'min_members': dept.find('minimale_teilnehmerzahl').text,
                      'max_members': dept.find('maximale_teilnehmerzahl').text, 'appointments': dept.find('anzahl_termine').text,
                      'begin_date': dept.find('beginn_datum').text, 'end_date': dept.find('ende_datum').text,
                      'target_audience': dept.find('zielgruppe').text, 'keywords': keywords,
                      'location': { 'name': dept.find('veranstaltungsort/name').text, 'country': dept.find('veranstaltungsort/adresse/land').text, 
                      'zipcode': dept.find('veranstaltungsort/adresse/plz').text, 'region': dept.find('veranstaltungsort/adresse/ort').text, 
                      'street': dept.find('veranstaltungsort/adresse/strasse').text, 'barrier_free': dept.find('veranstaltungsort/barrierefrei').text },
                      'price': { 'amount': dept.find('preis/betrag').text, 'discount_possible': dept.find('preis/rabatt_moeglich').text, 'price_reduced': dept.find('preis/zusatz').text },
                      'web': { 'type': dept.find('webadresse/typ').text, 'name': 'webadresse/name', 'uri': dept.find('webadresse/uri').text }
                      })
  except IOError:
    print("I/O error")
                                                                           
  print(rows)
  return rows

def register(data):
  

    client_id = '%s' % os.getpid()
    print(client_id)
    helper.create_kundenxml(client_id, data['username'], data['name'], data['surname'], 
                            data['street'], data['postcode'], data['city'], 
                            data['country'], data['email'], data['password'])
    return {'status': 'success', 'id': client_id}


model_all = api.model('Model', {
  'guid': fields.Integer,
  'number': fields.String,
  'name': fields.String(default='Course_name'),
  'subtitle': fields.String,
  'category': fields.Float,
  'min_members': fields.Integer,
  'max_members': fields.Integer,
  'appointments': fields.Integer,
  'begin_date': fields.Date,
  'end_date': fields.Date,
  'target_audience': fields.String,
  'keywords': fields.String,
  'location': fields.Nested(
    api.model('Location', {
      'name': fields.String,
      'country': fields.String,
      'zipcode': fields.String,
      'region': fields.String,
      'street': fields.String
    })
  ),
  'price': fields.Nested(
    api.model('Price', {
      'amount': fields.Float,
      'discount_possible': fields.Boolean,
      'price_reduced': fields.String
    })
  ),
  'web': fields.Nested(
    api.model('Webadress', {
      'type': fields.String,
      'name': fields.String,
      'uri': fields.String,
    })
  ),
})

model_reduced = api.model('Courses_reduced', {
  'guid': fields.Integer,
  'number': fields.String,
  'name': fields.String(default='Course_name'),
  'subtitle': fields.String,
})

@api.route('/courses')
class Courses(Resource):

  @api.doc('find_all_courses')
  @api.marshal_list_with(model_all)
  def get(self):
    #print(all_courses())
    response = jsonify(find_all_courses())
    return response.get_json(), 200

@api.route('/search')
@api.response(404, "Not found")
class CourseSearch(Resource):

  @api.doc('find_course')
  @api.marshal_list_with(model_all)
  def post(self):
    data = request.get_json()
    response = jsonify(find_course(data))
    return response.get_json(), 201
    
@api.route('/searchClID')
@api.response(404, "Not found")
class ClientIDSearch(Resource):

  @api.doc('find_client')
  def post(self):
    data = request.get_json()
    response = jsonify(find_client(data))
    return response.get_json(), 201

@api.route('/book')
@api.response(404, "Not found")
class CourseBook(Resource):

  @api.doc('book_course')
  #@api.marshal_list_with(model_all)
  def post(self):
    data = request.get_json()
    helper.add_kunde_to_course(data['guid'], session['user_id'])
    return "test", 201

# sign in
@api.route('/login')
@api.response(404, "Not found")
class Login(Resource):

  @api.doc('login')
  def post(self):
    data = request.get_json()

    if data['type'] == 'logout':
      if len(session) > 0:
        session.clear()
        response = { 'status' : 'logout success' }
        return response, 200
      else: 
        response = { 'status' : 'logout failed' }
        return response, 401

    elif data['type'] == 'login': 
      print(data)
      username = data['username']
      password = data['password']
      error = None
      default_user = {'username' : 'test', 'password' : '1234', 'id' : '12345'}

      # false data
      if default_user['username'] not in username:
          error = 'Incorrect username.'
      #elif not check_password_hash(default_user['password'], password):
      elif default_user['password'] not in password:
          error = 'Incorrect password.'

      if error is None:
        print('Logged in')
        session.clear()
        session['user_id'] = default_user['id']
        response = { 'status' : 'success', 'id':  session['user_id']}
        return response, 200

      response = { 'status' : 'authentication failed' }
      return response, 401

@api.route('/register')
@api.response(404, "Not found")
class Register(Resource):
  def post(self):
    data = request.get_json()
    response = { 'status' : register(data) }
    return response

# start page
@app.route('/index')
@api.doc('start_page')
def index():
  return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)