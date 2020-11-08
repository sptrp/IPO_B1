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

def path_constructor_guid(val):
  return "//veranstaltung[guid={}]" .format(val)

def path_constructor_nummer(val):
  return "//veranstaltung[nummer={}]" .format(val)

def path_constructor_name(name):
  return "//veranstaltung[contains(@name, {})]" .format(name)

# async = asynchronous function (coroutine; https://docs.python.org/3/glossary.html#term-coroutine)
async def demo():
      # connect() creates a client connection and receives a WebSocketClientProtocol object to send/receive WS messages
      async with websockets.connect("ws://localhost:8765") as ws:

          # navigation menu
          choice = '0'
          subchoice = '0'

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
              time.sleep(0.1)
              os._exit(1)   #Quelle: https://stackoverflow.com/questions/173278/is-there-a-way-to-prevent-a-systemexit-exception-raised-from-sys-exit-from-bei bypasses exceptions

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
                time.sleep(0.2)
                choice = input (config['menu']['format_chosen'].value)  
                
              # Read config file to get actual format value and make query
              config.read("config.cfg")
              calltype = config['calltype']['show_some_books'].value
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

            # show data
            elif choice == "1":
              # Call after format
              while choice != 'j':
                print(config['menu']['choose_format'].value)
                time.sleep(0.2)
                choice = input (config['menu']['format_chosen'].value) 
                config.read("config.cfg")
                format = config['misc']['format'].value  

              #Print submenu for data
              print(config['submenu2']['title'].value)
              print(config['submenu2']['alle'].value)
              print(config['submenu2']['guid'].value)
              print(config['submenu2']['nummer'].value)
              print(config['submenu2']['name'].value)
              print(config['submenu2']['untertitel'].value)
              print(config['submenu2']['back'].value)
              time.sleep(0.5)
              subchoice = input(config['submenu2']['choice'].value)
              print(subchoice)

              #show ALL courses
              if subchoice == "1":
                # Read config file to get query
                config.read("config.cfg")
                calltype = config['calltype']['show_all_courses'].value            
                data = "{}{}{}" .format(calltype,'path', format)
                await ws.send(data)
                # recv() receives data from the server
                response = await ws.recv()
                print("\n%s\n" % (config['misc']['all_courses'].value + response).encode())
                time.sleep(0.1)

              #sort with guid
              elif subchoice == "2":
                # Read config file to get query
                config.read("config.cfg")
                calltype = config['calltype']['show_some_books'].value
                path = path_constructor_guid(input("Bitte GUID angeben: "))      
                data = "{}{}{}" .format(calltype, path, format)
                await ws.send(data)
                # recv() receives data from the server
                response = await ws.recv()
                print("\n%s\n" % config['misc']['searched: '].value + response)
                time.sleep(0.1)

              #sort with nummer    
              elif subchoice == "3":
                  print("SUBCHOISE 3 ")
              #sort with names
              elif subchoice == "4":
                # Read config file to get query
                config.read("config.cfg")
                calltype = config['calltype']['show_some_books'].value
                path = path_constructor_name(input("Bitte Suchbegriff angeben: "))      
                data = "{}{}{}" .format(calltype, path, format)
                await ws.send(data)
                # recv() receives data from the server
                response = await ws.recv()
                print("\n%s\n" % config['misc']['searched'].value + response)
                time.sleep(0.1)

              #sort with subtitles    
              elif subchoice == "5":
                  print("E 5")                      
              else:
                  print("Looping!")
                  choice = 0

            else:
                print(config['menu']['repeat'].value)
                time.sleep(2)
          
          
# async only runs in an event_loop (https://cheat.readthedocs.io/en/latest/python/asyncio.html#event-loops)
# run_until_complete() gets demo coroutine as input to execute it
asyncio.get_event_loop().run_until_complete( demo() )



