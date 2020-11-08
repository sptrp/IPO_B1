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
import os

# logger
logging.basicConfig(level=logging.DEBUG)

xml = os.path.join(sys.path[0], 'kurse_snippet.xml')    #Quelle: https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
schema = os.path.join(sys.path[0], 'kurse.xsd')         #Damit es unter Linux, Windows und Mac laeuft
curr_format = ""

def xml_parser():
  tree = et.parse(xml)
  root = tree.getroot()
  output_string = et.tostring(root, encoding='utf8', method='xml')

  # Split message on 15 chunks, because it's too big (Nikolai's advice)
  first_chunk = output_string[0 : 123460]
  second_chunk = output_string[123460 : 246920]
  third_chunk = output_string[246920 : 493840]
  third_chunk = output_string[493840 : 987680]
  fourth_chunk = output_string[987680 : 1975360]
  fifth_chunk = output_string[1975360 : 2963040]
  sixth_chunk = output_string[2963040 : 3950720]
  seventh_chunk = output_string[3950720 : 4938400]
  eighth_chunk = output_string[4938400 : 5926080]
  ninth_chunk = output_string[5926080 : 6913760]
  ninth_chunk = output_string[5926080 : 6913760]
  tenth_chunk = output_string[6913760 : 7913760]
  eleventh_chunk = output_string[7913760 : 8913760]
  twelth_chunk = output_string[8913760 : 9913760]
  thirteenth_chunk = output_string[9913760 : 10913760]
  fourteenth_chunk = output_string[10913760 : 11913760]
  fifteenth_chunk = output_string[11913760 : -1]

  return fifteenth_chunk

# parse kurse_snippet and return csv
def csv_parser():
  tree = et.parse(xml)
  root = tree.getroot()

  rows = []
  spamreader = ''
  cols = ['Guid', 'Nummer', 'Name', 'Untertitel']
  # give the temp data distinct name
  file_name = 'courses.%s.csv' % os.getpid()

  try:
    with open(file_name, 'w', newline='', encoding="utf8") as file:
      # parse elements and write to csv
      for elem in root:

        rows.append({ "Guid": elem.find('guid').text, "Nummer": elem.find('nummer').text, 
                      "Name": elem.find('name').text, "Untertitel": elem.find('untertitel').text 
                    })
      dataframe = pd.DataFrame(rows, columns = cols) 
      dataframe.to_csv(file_name)
  except IOError:
    print("I/O error")
  finally:
    with open(file_name, encoding="utf8") as f:
      # place csv data in output string
      output_string = f.read() + '\n'
    # remove temp datei
    os.remove(file_name)
  
  return output_string 


# validator for incoming xml  
def xml_validator():
  # create parser from xsd schema
  with open(schema, 'rb') as f:
    schema_root = et.XML(f.read())
    val_schema = et.XMLSchema(schema_root)
    parser = et.XMLParser(schema=val_schema)

  try:
    with open(xml, 'r', encoding="utf8") as f:
      et.fromstring(f.read(), parser) 
    return True # return true if file is valid
  except et.XMLSchemaError: 
    return False # return false and exception if not

# select concrete element
def xml_element_selector(path):

  root = xml_parser()
  list = root.xpath(path)

  return list

def show_path_bookings(path):
  root = xml_parser()
  my_dict = {}
  rows = []
  tree = et.parse(xml)
  root = tree.getroot()
  cols = [' Name', ' Untertitel', ' Minimale Teilnehmerzahl', ' Maximale Teilnehmerzahl', ' Beginn Datum']
  # give the temp data distinct name
  file_name = 'my_courses.%s.csv' % os.getpid()

  # parse all found elements and make dict
  for targ in root.xpath(path): # https://stackoverflow.com/questions/21746525/get-all-parents-of-xml-node-using-python
    for dept in targ.xpath('ancestor-or-self::veranstaltung'):
      my_dict[dept[0].text] = { "Name" : dept[2].text, "Untertitel" : dept[3].text,
                                "Minimale Teilnehmerzahl" : dept[5].text,
                                "Maximale Teilnehmerzahl" : dept[6].text,
                                "Beginn Datum" : dept[8].text
                              } 
  try:
    with open(file_name, 'w', encoding="utf8") as file:
      for elem in my_dict:
        # parse elements and write to csv
        rows.append({ "Name": my_dict[elem]['Name'], "Untertitel": my_dict[elem]['Untertitel'],
                      "Minimale Teilnehmerzahl": my_dict[elem]['Minimale Teilnehmerzahl'], 
                      "Maximale Teilnehmerzahl": my_dict[elem]['Maximale Teilnehmerzahl'], 
                      "Beginn Datum": my_dict[elem]['Beginn Datum'] 
                    })
      dataframe = pd.DataFrame(rows, columns = cols) 
      dataframe.to_csv(file_name)
  except IOError:
      print("I/O error")
  finally:
    with open(file_name, encoding="utf8") as f:
      # place csv data in output string
      output_string = f.read() + '\n'
    # remove temp file
    os.remove(file_name)

  return output_string


# server
async def echo(websocket, path):
  async for message in websocket:

    calltype = message[:3]

    if (calltype == 'acs'):
      format = message[-3:]
      await websocket.send(xml_parser())
      
    elif (calltype == 'abk'):
      format = message[-3:]
      path = message[3:-3]
      print(path)
      await websocket.send(str(show_path_bookings(path)))
    
    elif (calltype == 'fgu'):
      format = message[-3:]
      path = message[3:-3]
      print(path)
      await websocket.send(str(show_path_bookings(path)))


asyncio.get_event_loop().run_until_complete( websockets.serve(echo, "localhost", 8765, max_size = None) )
print("Running service at https//:localhost:8765")
# run_forever: runs the event loop forever; end loop with stop() method or Ctrl-C
asyncio.get_event_loop().run_forever()