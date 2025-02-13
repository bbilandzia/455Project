#Websocket Server
# import libraries
#asynco
#websockets
import asyncio
import websockets
import ssl
import pathlib
#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve
print("yo")
async def hello(websocket):
    #print("homie")
    #name = await websocket.recv()
    #print(f"<<< {name}")

    #greeting = f"Hello {name}!"

    #await websocket.send(greeting)
    #print(f">>> {greeting}")
    while(1):
          name = await websocket.recv()
          print("them:: "+name)

          greeting = input("me::  ")

          await websocket.send(greeting)
          #print("them:: {greeting}")  
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhostpem= pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_cert_chain(localhostpem)

async def main():
    print("main")
    async with serve(hello, "localhost", 8765, ssl=ssl_context):
        print("inside main")
        await asyncio.get_running_loop().create_future()  # run forever
        print("does this work")

if __name__ == "__main__":
    print("yo")
    asyncio.run(main())
