#Websocket Server
# import libraries
#asynco
#websockets
import asyncio
import websockets
import ssl
import pathlib
from websockets.asyncio.server import serve
clients = set()

#print("yo")
async def hello(websocket):
    #print("homie")
    #name = await websocket.recv()
    await websocket.send("NAME????    ")
    name = await websocket.recv()
    clients.add(name)
    name = ""
    #print(f"<<< {name}")

    #greeting = f"Hello {name}!"

    #await websocket.send(greeting)
    #print(f">>> {greeting}")
    while(1): #creates a while loop that constantly waits for messages, and sends them as of now 
          name = await websocket.recv()
          print(name)
          await websocket.send(name)
          #for client in clients:
              #if client != websocket:
                  #await websocket.send(name)
          #await websocket.send("{name}")
          #greeting = input("me::  ")

          #await websocket.send(greeting)
          #print("them:: {greeting}")  
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhostpem= pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_cert_chain(localhostpem)

async def main():
    #print("main")
    async with serve(hello, "localhost", 8765, ssl=ssl_context): #this creates the server on the localhost on port 8765 and uses SSL_context for the ssl 
        print("inside main")
        await asyncio.get_running_loop().create_future()  # this makes it so it runs forever
        print("does this work")

if __name__ == "__main__":
    #print("yo")
    asyncio.run(main())
