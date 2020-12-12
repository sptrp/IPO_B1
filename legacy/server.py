""" 
B1 websocket server
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
import helper 

# logger
#logging.basicConfig(level=logging.DEBUG)

xml = os.path.join(sys.path[0], 'kurse.xml')  #Quelle: https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
schema = os.path.join(sys.path[0], 'kurse.xsd')         #Damit es unter Linux, Windows und Mac laeuft
request_schema = os.path.join(sys.path[0], 'request.xsd')  


# parse kurse and return xml or csv
def find_all_courses(format):
  tree = et.parse(xml)
  root = tree.getroot()
  chunk = []

  if (format == 'xml'):
    tree = helper.xml_trimmer(tree)
    root = tree.getroot()

    output_string = et.tostring(root, encoding="utf8")
    chunk.append(output_string[0 : 475860])
    chunk.append(output_string[475860 : 961720])
    chunk.append(output_string[961720 : -1])
    return chunk

  else: 
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


def find_my_bookings(format, path):
  joined_string = ""
  # check format
  if (format == 'xml'):
    tree = helper.xml_trimmer_mybooks(et.parse(xml))
    root = tree.getroot()
    elems = root.xpath(path)

    for targ in elems: 
      for dept in targ.xpath('ancestor-or-self::veranstaltung'):
        joined_string = joined_string + et.tostring(dept, encoding="unicode", pretty_print=True)

    return joined_string
    
  else:   
    my_dict = {}
    rows = []
    tree = et.parse(xml)
    root = tree.getroot()
    cols = [' Name', ' Untertitel', ' Minimale Teilnehmerzahl', ' Maximale Teilnehmerzahl', ' Beginn Datum', ' Anzahl Buchungen']
    # give the temp data distinct name
    file_name = 'my_courses%s.csv' % os.getpid()

    # parse all found elements and make dict
    for targ in root.xpath(path): # https://stackoverflow.com/questions/21746525/get-all-parents-of-xml-node-using-python
      for dept in targ.xpath('ancestor-or-self::veranstaltung'):
        my_dict[dept[0].text] = { "Name" : dept[2].text, 
                                  "Untertitel" : dept[3].text,
                                  "Minimale Teilnehmerzahl" : dept[5].text,
                                  "Maximale Teilnehmerzahl" : dept[6].text,
                                  "Beginn Datum" : dept[8].text,
                                  "Anzahl Buchungen": 'test'
                                }                                                                   
    try:
      with open(file_name, 'w') as file:
        for elem in my_dict:
          # parse elements and write to csv
          rows.append({ " Name": my_dict[elem]['Name'], " Untertitel": my_dict[elem]['Untertitel'],
                        " Minimale Teilnehmerzahl": my_dict[elem]['Minimale Teilnehmerzahl'], 
                        " Maximale Teilnehmerzahl": my_dict[elem]['Maximale Teilnehmerzahl'], 
                        " Beginn Datum": my_dict[elem]['Beginn Datum'],
                        " Anzahl Buchungen": my_dict[elem]['Anzahl Buchungen']  
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

def find_diverse_from_query(format, path, calltype=''):
  joined_string = ""
  # check format
  if (format == 'xml'):
    tree = helper.xml_trimmer(et.parse(xml))
    root = tree.getroot()
    elems = root.xpath(path)

    for targ in elems: 
      for dept in targ.xpath('ancestor-or-self::veranstaltung'):
        joined_string = joined_string + et.tostring(dept, encoding="unicode", pretty_print=True)

    return joined_string
    
  else:   
    my_dict = {}
    rows = []
    tree = et.parse(xml)
    root = tree.getroot()
    cols = [' Guid', ' Nummer', ' Name', ' Untertitel']
    # give the temp data distinct name
    file_name = 'my_courses%s.csv' % os.getpid()

    # parse all found elements and make dict
    for targ in root.xpath(path): # https://stackoverflow.com/questions/21746525/get-all-parents-of-xml-node-using-python
      for dept in targ.xpath('ancestor-or-self::veranstaltung'):
        my_dict[dept[0].text] = { "Guid" : dept[0].text, "Nummer" : dept[1].text,
                                  "Name" : dept[2].text,
                                  "Untertitel" : dept[3].text
                                }                                                                   
    try:
      with open(file_name, 'w') as file:
        for elem in my_dict:
          # parse elements and write to csv
          rows.append({ " Guid": my_dict[elem]['Guid'], " Nummer": my_dict[elem]['Nummer'],
                        " Name": my_dict[elem]['Name'], " Untertitel": my_dict[elem]['Untertitel'],
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

# validator for incoming request  
def xml_validator(input, schema):
    # create parser from xsd schema
    with open(schema, 'rb') as s:
      schema_root = et.XML(s.read())
      val_schema = et.XMLSchema(schema_root)
      parser = et.XMLParser(schema=val_schema)

    try:
      # pass request
      et.fromstring(input, parser) 
      return True # return true if file is valid
    except et.XMLSyntaxError: 
      print("Request Fehler: Falscher Request") # return exception and error message if not

# server
async def echo(websocket, path):
  async for message in websocket:
    
    # validate request
    if xml_validator(message, request_schema):

      tree = et.ElementTree(et.fromstring(message))
      # parse format and calltype from request
      format = tree.xpath('//format')[0].text
      calltype = tree.xpath('//calltype')[0].text

      if (calltype == 'acs'):
          if (format == 'xml'):
            response = find_all_courses(format)

            for elem in response:
              await websocket.send(elem)
          else: 
            await websocket.send(str(find_all_courses(format)))

      elif (calltype == 'sse'):
        elem = tree.xpath('//element')[0].text
        value = tree.xpath('//value')[0].text
        # build path
        if (elem == 'divers'):
          path = helper.path_constructor_divers(value)
        else: 
          path = helper.path_constructor_elem(elem, value) 

        await websocket.send(find_diverse_from_query(format, path, calltype))

      elif (calltype == 'mcs'):
        # parse client id from request
        client_id = tree.xpath('//client')[0].text
        # build path
        path = helper.path_constructor_book(client_id)
        await websocket.send(str(find_my_bookings(format, path)))

      elif (calltype == 'bwg'):

        # parse client id from request
        client_id = tree.xpath('//client')[0].text
        guid = tree.xpath('//guid')[0].text
        try:
          helper.add_kunde_to_course(guid, client_id)
        except:
          await websocket.send('Leider wurde die GUID nicht gefunden.')
        else:
          await websocket.send('Buchung erfolgreich!')

    else:
        await websocket.send('Falscher Request')

asyncio.get_event_loop().run_until_complete( websockets.serve(echo, "localhost", 8765, max_size = 2**25, ping_timeout=10000000) )
print("Running service at https//:localhost:8765")
asyncio.get_event_loop().run_forever()