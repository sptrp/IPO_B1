"""
Example uses a WebSockets server for testing purposes (see also https://www.websocket.org/echo.html).
The server simply replies with xml or csv.
"""

# TODO: 
# pip install asyncio
# pip install websockets
# pip install configupdater

import asyncio
import websockets
import time
import os
from configupdater import ConfigUpdater

# read config file
config = ConfigUpdater()
config.read("config.cfg")

# client id 
client_id = os.getpid()

def path_constructor(elem, val):
  return "//veranstaltung/buchung[{}={}]" .format(elem, val)

# async = asynchronous function (coroutine; https://docs.python.org/3/glossary.html#term-coroutine)
async def demo():
      # connect() creates a client connection and receives a WebSocketClientProtocol object to send/receive WS messages
      async with websockets.connect("ws://localhost:8765") as ws:

          # navigation menu
          choice = '0'

          while choice != '9':
            # Greeting and format
            print("Client %s runs" % client_id)

            # Menu
            print(config['menu']['greet'].value)
            print(config['menu']['data'].value)
            print(config['menu']['book'].value)
            print(config['menu']['my_books'].value)
            print(config['menu']['end'].value)
            
            choice = input (config['menu']['choice'].value)

            # Exit program
            if choice == '9':
              print(config['menu']['bye'].value)
              time.sleep(2)
              exit()

            elif choice == "5":
                print("Go to another menu")
                second_menu()

            elif choice == "4":
                print("Do Something 4")

            # Show my booking
            elif choice == "3":
              # Call after format
              while choice != 'j':
                print(config['menu']['choose_format'].value)
                time.sleep(2)
                choice = input (config['menu']['format_chosen'].value)  
                
              # Read config file to get actual format value and make query
              config.read("config.cfg")
              calltype = config['calltype']['show_my_books'].value
              path = path_constructor(config['misc']['path_client'].value, client_id)              
              format = config['misc']['format'].value

              data = "{}{}{}" .format(calltype, path, format)

              await ws.send(data)
              # recv() receives data from the server
              response = await ws.recv()
              print("\n%s\n" % config['misc']['my_courses'].value + response)
              time.sleep(2)

            elif choice == "2":
                print("Do Something 2")

            # Show all courses
            elif choice == "1":
              # Call after format
              while choice != 'j':
                print(config['menu']['choose_format'].value)
                time.sleep(2)
                choice = input (config['menu']['format_chosen'].value) 
                
              # Read config file to get actual format value and make query
              config.read("config.cfg")
              calltype = config['calltype']['show_all_courses'].value            
              format = config['misc']['format'].value

              data = "{}{}" .format(calltype, format)

              await ws.send(data)
              # recv() receives data from the server
              response = await ws.recv()
              print("\n%s\n" % config['misc']['all_courses'].value + response)
              time.sleep(2)

            else:
                print("I don't understand your choice.")
          
          
# async only runs in an event_loop (https://cheat.readthedocs.io/en/latest/python/asyncio.html#event-loops)
# run_until_complete() gets demo coroutine as input to execute it
asyncio.get_event_loop().run_until_complete( demo() )



