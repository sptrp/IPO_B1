""" Simple websocket server
"""

# TODO: 
# pip install asyncio
# pip install websockets
# pip install xmltodict
# pip install pandas

import asyncio
import websockets
import lxml.etree as et
import csv
import xmltodict
import pandas as pd  

def xml_parser():
  xml = "/Users/Sptrp/Desktop/IPO_B1/kurse_snippet.xml"
  tree = et.parse(xml)
  root = tree.getroot()
  return root

def csv_parser():
  xml = "/Users/Sptrp/Desktop/IPO_B1/kurse_snippet.xml"
  tree = et.parse(xml)
  root = tree.getroot()

  # convert to dict
  #xmlstr = et.tostring(root, encoding='utf-8', method='xml')
  #xml_dict = dict(xmltodict.parse(xmlstr))

  cols = ['Guid', 'Nummer', 'Name', 'Untertitel']
  rows = []

  with open('mycsvfile.csv','w', newline='') as file:

    #parse einzelne Elemente
    for elem in root:
      guid = elem.find('guid').text
      nummer = elem.find('nummer').text
      name = elem.find('name').text
      untertitel = elem.find('untertitel').text

      rows.append({"Guid": guid, "Nummer": nummer, "Name": name, "Untertitel": untertitel})

      df = pd.DataFrame(rows, columns = cols) 
      df.to_csv('mycsvfile.csv')

  return "test"


async def echo(websocket, path):
    async for message in websocket:

        # Print client message at server console
        print(f"The client says: {message}")
        #xmlstr = et.tostring(csv_parser(), encoding='utf8', method='xml')

        # ... and sent it back to client
        await websocket.send(csv_parser())


asyncio.get_event_loop().run_until_complete( websockets.serve(echo, "localhost", 8765) )

print(f"Running service at https//:localhost:8765")
# run_forever: runs the event loop forever; end loop with stop() method or Ctrl-C
asyncio.get_event_loop().run_forever()
