""" 
B1 websocket server
"""

# TODO: 
# pip install flask
# pip install flask_cors (to get rid of cors https://stackoverflow.com/questions/20035101/why-does-my-javascript-code-receive-a-no-access-control-allow-origin-header-i)
# pip install pandas
# pip install flask_restx (for automatic documentation etc.)
# pip install xmltodict


from http.server import HTTPServer, BaseHTTPRequestHandler
from flask import Flask, json, request, jsonify, Blueprint, render_template # https://stackovetrflow.com/questions/49964340/geting-flask-json-response-as-an-html-table
from flask_restx import Api, Resource, fields
from flask_cors import CORS, cross_origin

import pandas as pd  
import lxml.etree as et
import os
import sys
import helper
import logging 

from json import dumps

# logger
# logging.basicConfig(level=logging.DEBUG)

xml = os.path.join(sys.path[0], 'data/kurse.xml')  #Quelle: https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
schema = os.path.join(sys.path[0], 'data/kurse.xsd')         #Damit es unter Linux, Windows und Mac laeuft
request_schema = os.path.join(sys.path[0], 'data/request.xsd')  

# server
app = Flask(__name__)
# use blueprints to avoid CORS errors (Nikolai's advice)
bp = Blueprint('api', __name__, url_prefix='/api/')
api = Api(bp)
app.register_blueprint(bp)


# parse course and return json
def find_all_courses():
  tree = et.parse(xml)
  root = tree.getroot()
  rows = []

  try:
    # parse elements and write to json
    for dept in root:

      # index.append(elem.find('guid').text)
      rows.append({ 'guid':dept.find('guid').text, 'number': dept.find('nummer').text, 
                    'name': dept.find('name').text, 'subtitle': dept.find('untertitel').text,
                    'category': dept.find('dvv_kategorie').text, 'min_members': dept.find('minimale_teilnehmerzahl').text,
                    'max_members': dept.find('maximale_teilnehmerzahl').text, 'appointments': dept.find('anzahl_termine').text,
                    'begin_date': dept.find('beginn_datum').text, 'end_date': dept.find('ende_datum').text,
                    'target_audience': dept.find('zielgruppe').text, 'keywords': { 'keyword': kw.text for kw in dept.findall('schlagwort') },
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

  print(request)
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
        for kw in dept.findall('schlagwort'):
          print({'keyword': kw.text}) 
        rows.append({ 'guid':dept.find('guid').text, 'number': dept.find('nummer').text, 
                      'name': dept.find('name').text, 'subtitle': dept.find('untertitel').text,
                      'category': dept.find('dvv_kategorie').text, 'min_members': dept.find('minimale_teilnehmerzahl').text,
                      'max_members': dept.find('maximale_teilnehmerzahl').text, 'appointments': dept.find('anzahl_termine').text,
                      'begin_date': dept.find('beginn_datum').text, 'end_date': dept.find('ende_datum').text,
                      'target_audience': dept.find('zielgruppe').text, 'keywords': { 'keyword': kw.text for kw in dept.findall('schlagwort') }, #TODO: KEYWORDS
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
  'keywords': fields.Nested(
    api.model('Keywords', {
      'keyword': fields.String,
    })
  ),
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
class Courses(Resource):

  @api.doc('find_course')
  @api.marshal_list_with(model_all)
  def post(self):
    data = request.get_json()
    response = jsonify(find_course(data))
    return response.get_json(), 201

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)