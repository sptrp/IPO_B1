"""
B1 websocket client
"""

# TODO: 
# pip install asyncio
# pip install websockets
# pip install configupdater

import asyncio
import websockets
import time
import os
import helper 
from configupdater import ConfigUpdater
import lxml.etree as et

# client id 
client_id = os.getpid()

# create temporary config file
config = ConfigUpdater()
config_path = "config.%s.cfg" % os.getpid()
helper.create_config(config, config_path)


# async = asynchronous function (coroutine; https://docs.python.org/3/glossary.html#term-coroutine)
async def demo():
      # connect() creates a client connection and receives a WebSocketClientProtocol object to send/receive WS messages
      async with websockets.connect("ws://localhost:8765") as ws:

          # navigation menu
          choice = '0'
          subchoice = '0'

          while choice != '9':
            # Greeting and format
            print("Client %s runs" % client_id)  #testet client id

            # Menu
            print(config['menu']['greet'].value)
            print(config['menu']['data'].value)
            print(config['menu']['book'].value)
            print(config['menu']['my_books'].value)
            print(config['menu']['menu_choose_format'].value)
            print(config['menu']['end'].value)
            
            choice = input (config['menu']['choice'].value)

            # Exit program
            if choice == '9':
              print(config['menu']['bye'].value)
              time.sleep(0.1)
              os.remove(config_path)
              os._exit(1)   #Quelle: https://stackoverflow.com/questions/173278/is-there-a-way-to-prevent-a-systemexit-exception-raised-from-sys-exit-from-bei bypasses exceptions

            elif choice == "5":
              print("Do Something 4")

            elif choice == "4":
              helper.config_switcher(config, config_path)

            # Show my booking
            elif choice == "3":           
              # Read config file to get actual format value and make query
              config.read(config_path)
              calltype = config['calltype']['show_my_courses'].value

              # build request
              request = helper.create_request(config, calltype, client_id)
              await ws.send(et.tostring(request, encoding='utf8', method='xml'))
              # recv() receives data from the server
              response = await ws.recv()
              print("\n%s\n" % config['misc']['my_courses'].value + response)
              time.sleep(2)

            elif choice == "2":
              # Read config file to get actual format value and make query
              config.read(config_path)
              calltype = config['calltype']['show_my_courses'].value
              
              request = helper.create_request(config, calltype, client_id)
            
              print(et.tostring(request, encoding='utf8', method='xml'))

            # show data
            elif choice == "1":
              #Print submenu for data
              print(config['submenu2']['title'].value)
              print(config['submenu2']['alle'].value)
              print(config['submenu2']['guid'].value)
              print(config['submenu2']['nummer'].value)
              print(config['submenu2']['name'].value)
              print(config['submenu2']['attribute'].value)
              print(config['submenu2']['back'].value)
              time.sleep(0.5)
              subchoice = input(config['submenu2']['choice'].value)
              print(subchoice)

              #show ALL courses
              if subchoice == "1":
                # Read config file to get actual format value and make query
                config.read(config_path)
                calltype = config['calltype']['show_all_courses'].value
                format = config['misc']['format'].value

                # build request
                request = helper.create_request(config, calltype, client_id)
                await ws.send(et.tostring(request, encoding='utf8', method='xml'))
                
                if (format == 'xml'):
                  for i in range(17):           
                    # recv() receives data from the server
                    response = await ws.recv()
                    print(response)
                    #print("\n%s\n" % config['misc']['my_courses'].value + response)
                else:
                  response = await ws.recv()
                  print("\n%s\n" % config['misc']['my_courses'].value + response)
                time.sleep(2)

              #sort with guid
              elif subchoice == "2":
                # Read config file to get query
                config.read(config_path)
                calltype = config['calltype']['show_some_elems'].value
                value = input(config['submenu2']['choice_guid'].value)

                # build request 
                request = helper.create_elem_request(config, "guid", calltype, value, client_id)
                await ws.send(et.tostring(request, encoding='utf8', method='xml'))
                # recv() receives data from the server
                response = await ws.recv()
        
                print("\n%s\n" % config['misc']['searched'].value + response)
                time.sleep(0.1)

              #sort with nummer    
              elif subchoice == "3":
                # Read config file to get query
                config.read(config_path)
                calltype = config['calltype']['show_some_elems'].value
                value = input(config['submenu2']['choice_nummer'].value)

                # build request 
                request = helper.create_elem_request(config, "nummer", calltype, value, client_id)
                await ws.send(et.tostring(request, encoding='utf8', method='xml'))
                # recv() receives data from the server
                response = await ws.recv()

                print("\n%s\n" % config['misc']['searched'].value + response)
                time.sleep(0.1)

              #sort with names
              elif subchoice == "4":
                # Read config file to get query
                config.read(config_path)
                calltype = config['calltype']['show_some_elems'].value
                value = input(config['submenu2']['choice_name'].value)

                # build request 
                request = helper.create_elem_request(config, "name", calltype, value, client_id)
                await ws.send(et.tostring(request, encoding='utf8', method='xml'))
                # recv() receives data from the server
                response = await ws.recv()

                print("\n%s\n" % config['misc']['searched'].value + response)
                time.sleep(0.1)

              #sort with stichwort
              elif subchoice == "5":
                # Read config file to get query
                config.read(config_path)
                calltype = config['calltype']['show_some_elems'].value
                value = input(config['submenu2']['choice_divers'].value)

                # build request 
                request = helper.create_elem_request(config, "divers", calltype, value, client_id)
                await ws.send(et.tostring(request, encoding='utf8', method='xml'))
                # recv() receives data from the server
                response = await ws.recv()

                print("\n%s\n" % config['misc']['searched'].value + response)
                time.sleep(0.1)

              elif subchoice == "6":
                  print("Hauptmenu....")
                  time.sleep(1)
                  choice = 0

              else:
                print(config['menu']['repeat'].value)
                time.sleep(2)

            else:
                print(config['menu']['repeat'].value)
                time.sleep(2)
          
          
# async only runs in an event_loop (https://cheat.readthedocs.io/en/latest/python/asyncio.html#event-loops)
# run_until_complete() gets demo coroutine as input to execute it
asyncio.get_event_loop().run_until_complete( demo() )



