#!/usr/bin/env python

import asyncio
import websockets
from websockets.asyncio.client import connect
import ssl
import pathlib

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhostpem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_verify_locations(localhostpem)
async def hello():
    print("yo")
    uri = "wss://127.0.0.1:8765"
    port = 8769

    async with connect(uri, ssl=ssl_context) as websocket:
        #name = input("What's your name? ")

        #await websocket.send(name)
        #print(f">>> {name}")

        #greeting = await websocket.recv()
        #print(f"<<< {greeting}")
        while(True):
            message = input("Me:: ")
            #print(message)
            await websocket.send(message)
            returned = await websocket.recv()
            print("Them::  "+returned)

asyncio.run(hello())