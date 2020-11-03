#!/usr/bin/env python3

""" Simple websocket server
"""

# TODO: 
# pip install asyncio
# pip install websockets

import asyncio
import websockets
import xml.etree.ElementTree as et

def xml_parser():
  xml = "/Users/Sptrp/Desktop/IPO_B1/kurse_snippet.xml"
  tree = et.parse(xml)
  root = tree.getroot()
  return root

async def echo(websocket, path):
    async for message in websocket:

        # Print client message at server console
        print(f"The client wants courses")

        xmlstr = et.tostring(xml_parser(), encoding='utf8', method='xml')

        # ... and sent it back to client
        await websocket.send(xmlstr)

# get_event_loop: low-level function to create an event loop instance
# run_until_complete: runs until the future (see argument) has completed
# websockets.serve: creates, starts, and returns a WebSocket server; 'echo' is a WebSocket handler
asyncio.get_event_loop().run_until_complete( websockets.serve(echo, "localhost", 8765) )

print(f"Running service at https//:localhost:8765")
# run_forever: runs the event loop forever; end loop with stop() method or Ctrl-C
asyncio.get_event_loop().run_forever()
