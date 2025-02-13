#Websocket Server
# import libraries
#asynco
#websockets
import asyncio
import websockets
#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve
print("yo")
async def hello(websocket, path):
    print("homie")
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")

async def main():
    print("main")
    async with serve(hello, "localhost", 8765):
        print("inside main")
        await asyncio.get_running_loop().create_future()  # run forever
        print("does this work")

if __name__ == "__main__":
    print("yo")
    asyncio.run(main())
