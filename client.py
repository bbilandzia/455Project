#!/usr/bin/env python

import asyncio
import websockets
from websockets.asyncio.client import connect

async def hello():
    print("yo")
    uri = "ws://127.0.0.1:8765"
    port = 8769
    async with connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

asyncio.run(hello())