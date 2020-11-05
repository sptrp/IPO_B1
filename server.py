""" B1 websocket server
"""

# TODO: 
# pip install asyncio
# pip install websockets
# pip install pandas
# pip install lxml

import asyncio
import websockets
import logging
import pandas as pd  
import csv
import lxml.etree as et
import sys

# logger
logging.basicConfig(level=logging.DEBUG)

xml = "/Users/Sptrp/Desktop/IPO_B1/kurse_snippet.xml"
schema = "/Users/Sptrp/Desktop/IPO_B1/kurse.xsd"

def xml_parser():
  tree = et.parse(xml)
  root = tree.getroot()
  return root

# parse kurse_snippet and return csv
def csv_parser():
  tree = et.parse(xml)
  root = tree.getroot()

  cols = ['Guid', 'Nummer', 'Name', 'Untertitel']
  rows = []
  spamreader = ''

  with open('mycsvfile.csv', 'w', newline='') as file:
    # parse elements and write to csv
    for elem in root:

      rows.append({ "Guid": elem.find('guid').text, "Nummer": elem.find('nummer').text, 
                    "Name": elem.find('name').text, "Untertitel": elem.find('untertitel').text 
                  })
    dataframe = pd.DataFrame(rows, columns = cols) 
    dataframe.to_csv('mycsvfile.csv')

  with open('mycsvfile.csv') as f:
    output_string = f.read() + '\n'

  return output_string 


# validator for incoming xml  
def xml_validator():
  # create parser from xsd schema
  with open(schema, 'rb') as f:
    schema_root = etree.XML(f.read())
    val_schema = etree.XMLSchema(schema_root)
    parser = etree.XMLParser(schema=val_schema)

  try:
    with open(xml, 'r') as f:
      etree.fromstring(f.read(), parser) 
    return True # return true if file is valid
  except etree.XMLSchemaError: 
    return False # return false and exception if not

# select concrete element
def xml_element_selector(path):

  root = xml_parser()
  list = root.xpath(path)

  return list

def show_my_bookings(path):
  root = xml_parser()
  my_dict = {}
  csv_file = "courses.csv"
  cols = ['Name', 'Untertitel', 'Minimale Teilnehmerzahl', 'Maximale Teilnehmerzahl', 'Beginn Datum']
  rows = []

  # parse all found elements and make dict
  for targ in root.xpath(path): # https://stackoverflow.com/questions/21746525/get-all-parents-of-xml-node-using-python
    for dept in targ.xpath('ancestor-or-self::veranstaltung'):
      my_dict[dept[0].text] = { "Name" : dept[2].text, "Untertitel" : dept[3].text,
                                "Minimale Teilnehmerzahl" : dept[5].text,
                                "Maximale Teilnehmerzahl" : dept[6].text,
                                "Beginn Datum" : dept[8].text
                              } 
  try:
    with open('courses.csv', 'w', newline='') as file:
      for elem in my_dict:
        # parse elements and write to csv
        rows.append({ "Name": my_dict[elem]['Name'], "Untertitel": my_dict[elem]['Untertitel'],
                      "Minimale Teilnehmerzahl": my_dict[elem]['Minimale Teilnehmerzahl'], 
                      "Maximale Teilnehmerzahl": my_dict[elem]['Maximale Teilnehmerzahl'], 
                      "Beginn Datum": my_dict[elem]['Beginn Datum'] 
                    })
      dataframe = pd.DataFrame(rows, columns = cols) 
      dataframe.to_csv('courses.csv')
  except IOError:
      print("I/O error")

  return "my_dict"


# server
async def echo(websocket, path):
    async for message in websocket:
        # handle format query
        if (message == "csv"):
          await websocket.send(csv_parser())
        else:
          print(message) 
          await websocket.send(str(show_my_bookings(message)))


asyncio.get_event_loop().run_until_complete( websockets.serve(echo, "localhost", 8765) )
print(f"Running service at https//:localhost:8765")
# run_forever: runs the event loop forever; end loop with stop() method or Ctrl-C
asyncio.get_event_loop().run_forever()
