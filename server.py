""" B1 websocket server
"""

# TODO: 
# pip install asyncio
# pip install websockets
# pip install pandas

import asyncio
import websockets
import xml.etree.ElementTree as et
import pandas as pd  

xml = "/Users/Sptrp/Desktop/IPO_B1/kurse_snippet.xml"

def xml_parser():
  tree = et.parse(xml)
  root = tree.getroot()
  return root

def csv_parser():
  tree = et.parse(xml)
  root = tree.getroot()

  cols = ['Guid', 'Nummer', 'Name', 'Untertitel']
  rows = []

  with open('mycsvfile.csv','w', newline='') as file:
    # parse einzelne Elemente
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

        # Formatanfrage bearbeiten
        if (message == "csv"):
          await websocket.send(csv_parser())
        else: 
          await websocket.send(xml_parser())


asyncio.get_event_loop().run_until_complete( websockets.serve(echo, "localhost", 8765) )

print(f"Running service at https//:localhost:8765")
# run_forever: runs the event loop forever; end loop with stop() method or Ctrl-C
asyncio.get_event_loop().run_forever()
