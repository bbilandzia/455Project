#!/usr/bin/env python3
import asyncio
import websockets
import ssl
import pathlib
from datetime import datetime
#clients = set()

# Global variables
connected_users = {}    # count of connected users to chat
message_counts = {}     # count of messages sent by each user in the last minute
last_reset = {}         # time of last message sent by each user
RATE_LIMIT = 30         # messages per minute

# Test users; can create more users by adding to this dictionary
USERS = {
    "testuser1" : "password123",
    "testuser2" : "password456"
}

# Prevent users from spamming chat
def check_rate_limit(username):
    current_time = datetime.now()
    if username not in last_reset:
        # add username to last_reset array
        last_reset[username] = current_time
        message_counts[username] = 0
    else:
        time_diff = (current_time - last_reset[username]).total_seconds()
        if time_diff > 60:
            last_reset[username] = current_time
            message_counts[username] = 0
        elif message_counts[username] >= RATE_LIMIT:
            return False
    message_counts[username] += 1
    return True

# Sends to all connected users in chat
async def server_broadcast(message):
    for username, websocket in list(connected_users.items()):
        try:
            await websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            print(f"Connection with {username} closed.")
            del connected_users[username]

# Handles authentication and client connection
async def hello(websocket):
    username = None
    try:
        auth_msg = await websocket.recv()
        username, password = auth_msg.split('\n')

        # authentication failure
        if username not in USERS or USERS[username] != password:
            await websocket.send("Authentication failed.")
            return
        
        # authentication success
        connected_users[username] = websocket
        await websocket.send("Authentication successful!")
        await server_broadcast(f"{username} has joined the chat.")
    
    # message handling
        while(1): #creates a while loop that constantly waits for messages, and sends them as of now 
            message = await websocket.recv()
            print(f"{username}: {message}")

            # check rate limiting
            if not check_rate_limit(username):
                await websocket.send("Error: You're sending too many messages!")
                continue

            chat_msg = f"{username}: {message}"
            await server_broadcast(chat_msg)
            await websocket.send(chat_msg)
    # error handling
    except Exception as e:
        print(f"Error: {e}")
    # logout user if they leave the chat
    finally:
        if username in connected_users:
            await server_broadcast(f"{username} has left the chat.")
            connected_users.pop(username, None)

# SSL configuration
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhostpem= pathlib.Path(__file__).with_name("localhost.pem")
    ## NOTE: may need to manually generate certificates if testing on multiple devices 
    ## certs seem to certify for only 10 min? 
    ## included script cert-generator.sh in case our default certs fail to certify
    ## generate localhost.pem on server device and copy to client devices
    ## note the IP address of the server device!! Needed to connect via client
ssl_context.load_cert_chain(localhostpem)

async def main():
    async with websockets.serve(hello, "localhost", 8765, ssl=ssl_context): #this creates the server on the localhost on port 8765 and uses SSL_context for the ssl 
        print("inside main")
        print("SecureChat server running on wss://localhost:8765")
        print("Please use the following credentials to test chat functionality:")
        print("\n\tUser 1: testuser1 / password123")
        print("\tUser 2: testuser2 / password456")
        print("\nTo close connection, press ctrl + c.")
        await asyncio.get_running_loop().create_future()  # this makes it so it runs forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer shutting down...")
