#!/usr/bin/env python
import asyncio
import websockets
import ssl
import pathlib

# SSL configuration
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhostpem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_verify_locations(localhostpem)

# Connect to server
async def connect_to_server():
    server_ip = input("Enter server IP (or press Enter for localhost): ") or "localhost"
    server_address = f"wss://{server_ip}:8765"

    try:
        # user login
        connection = await websockets.connect(server_address, ssl=ssl_context)
        print("\n Please log in:")
        username = input("Username: ")
        password = input("Password: ")

        await connection.send(f"{username}\n{password}")

        result = await connection.recv()
        if result == "Authentication successful!":
            print("Successfully logged in.")
            return connection, username
        else:
            print("\nLogin failed - wrong username or password.")
            await connection.close()
            return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

#able to send messages
async def send(websocket, username):
    print(f"Connected to server. You can now send messages.")
    print(f"\tType /quit to leave the chat.")
    while(True):
        message = input("Me:: ")
        if message == "/quit":
            await websocket.close()
            break
        await websocket.send(message)

#able to receive messages
async def receive(websocket, user):
    while(True):
        returned = await websocket.recv()
        print(f"{user} {returned}")  # prints received message
        print(f"{user} ", end = '', flush = True) # clear out the buffer, sets up for next message

async def main():
    connection, username = await connect_to_server()
    rectask = asyncio.create_task(receive(connection, username))

    try:
       # sendtask = asyncio.create_task(send(websocket,user)) This isn't working atm but I can get 2 clients connected now so that's cool
        await send(connection, username)
    finally:
        rectask.cancel()
        await connection.close()
    #await asyncio.wait([sendtask,rectask],return_when=asyncio.FIRST_COMPLETED)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nConnection terminated by user.")