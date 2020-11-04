"""
Example uses a WebSockets server for testing purposes (see also https://www.websocket.org/echo.html).
The server simply replies with xml or csv.
"""

# TODO: 
# pip install asyncio
# pip install websockets

import asyncio
import websockets

# async = asynchronous function (coroutine; https://docs.python.org/3/glossary.html#term-coroutine)
async def demo():

    # connect() creates a client connection and receives a WebSocketClientProtocol object to send/receive WS messages
    # "async with" closes connection at context switch automatically (https://www.python.org/dev/peps/pep-0492/#asynchronous-context-managers-and-async-with)
    async with websockets.connect("ws://localhost:8765") as ws:

        # send "csv" to get csv response, or smth else to xml response
        await ws.send("asd")

        # recv() receives data from the server
        response = await ws.recv()
        print(response)

# async only runs in an event_loop (https://cheat.readthedocs.io/en/latest/python/asyncio.html#event-loops)
# run_until_complete() gets demo coroutine as input to execute it
asyncio.get_event_loop().run_until_complete( demo() )

