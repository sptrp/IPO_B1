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
#import xml.etree.ElementTree as et
import pandas as pd  
import csv
import lxml.etree as et

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
    # parse elements
    for elem in root:
      guid = elem.find('guid').text
      nummer = elem.find('nummer').text
      name = elem.find('name').text
      untertitel = elem.find('untertitel').text

      rows.append({"Guid": guid, "Nummer": nummer, "Name": name, "Untertitel": untertitel})

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
def xml_selector(path):

  root = xml_parser()
  list = root.xpath(path)

  return list



async def echo(websocket, path):
    async for message in websocket:
        # handle format query
        if (message == "csv"):
          await websocket.send(csv_parser())
        else:
          print(message) 
          await websocket.send(str(xml_selector(message)))


asyncio.get_event_loop().run_until_complete( websockets.serve(echo, "localhost", 8765) )
print(f"Running service at https//:localhost:8765")
# run_forever: runs the event loop forever; end loop with stop() method or Ctrl-C
asyncio.get_event_loop().run_forever()
