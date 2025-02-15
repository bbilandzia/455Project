# 455Project: SecureChat

## Project Scope
SecureChat serves as a foundational product for SecureTech, a company specializing in software for distributed teams. This real-time communication tool aims to use secure and efficient communicaiton without relying on third-party services such as Slack or Teams. This system focuses on secure WebSocket-based communication.

Version 1.0 will be a proof-of-concept (POC), utilizing only two users communicating on the system.

## Key Features
1. Real-time messaging
2. Secure Connection
3. User Authentication
4. Rate Limiting
5. Connection Handling

## How to use
1. Navigate to the project folder on the device you'll be using as the server. Start the server via terminal:
```
python3 server.py
```
2. Server Terminal should populate with this:
```
SecureChat server running on wss://localhost:8765
Please use the following credentials to test chat functionality:
    User 1: testuser1 / password123
    User 2: testuser2 / password456

To close connection, press ctrl + c.
```
3. Open a new terminal for the client. Start the client via terminal:
```
python3 client.py
```
4. Client Terminal will ask for Server IP. Enter your server device's IP (starts with 192.168.x.x or 10.211.x.x).**
5. Client Terminal will now ask for login. Available test user logins are found in the Server Terminal upon server startup.
6. If authentication is successful, you are now ready to start chatting!

# **Included is a pre-designated certificate, **localhost.pem**. Should this certificate fail to certify on your device upon login, run the script cert-generator.sh to generate a certificate for your server device. To run:
```
chmod +x cert-generator.sh
./cert-generator.sh
```
Script generates key.pem, cert.pem, and localhost.pem. Share the localhost.pem with other client devices.
