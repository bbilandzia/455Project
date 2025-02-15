#!/usr/bin/env python

import asyncio
import websockets
from websockets.asyncio.client import connect
import ssl
import pathlib

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhostpem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_verify_locations(localhostpem)
#able to send messages
async def send(websocket, user):
    while(True):
        message = input("Me:: ")
            #print(message)
        await websocket.send(user+ " : "+ message)
#able to receive messages
async def receive(websocket):
    while(True):
        returned = await websocket.recv()
        print(returned)
async def hello():
    print("yo")
    uri = "wss://127.0.0.1:8765"
    port = 8769
    async with connect(uri, ssl=ssl_context) as websocket:
        await websocket.recv()
        user = input("Enter Name: ")
        await websocket.send(user)
        #this lets both tasks run together 
        rectask = asyncio.create_task(receive(websocket))
        sendtask = asyncio.create_task(send(websocket,user)) #This isn't working atm but I can get 2 clients connected now so that's cool
        
        await asyncio.wait([sendtask,rectask],return_when=asyncio.FIRST_COMPLETED)

asyncio.run(hello())