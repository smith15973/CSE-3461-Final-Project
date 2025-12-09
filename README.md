# CSE-3461-Final-Project

A real-time messaging app built with Python TCP sockets. You can chat with multiple people and send private DMs.

## Message types:
- `CHAT|sender|message` - public messages everyone sees
- `DIRECT|sender|message` - private DMs
- `USERLIST|user1,user2,user3` - who's online


## Files
- `TCPServer.py` - the server that handles all connections
- `TCPClient.py` - the client you run to connect
- `message_protocol.py` - shared code for sending/receiving messages properly
- `ChatUI.py` - the chat interface

## How to Run
Start the server:
``` bash
python TCPServer.py
```
Connect clients (open new terminals for each):
``` bash
python TCPClient.py
```

## Technical Stuff
The main challenge was preventing message merging in TCP streams. We solved it by prefixing each message with its length (4 bytes). The receiver reads the length first, then reads exactly that many bytes for the message.

The server uses threading to handle multiple clients and keeps a dictionary mapping sockets to usernames. Using conditionals for the start of the message, the message is categorized by message type, and using a username list to ensure there is no repeat or username that does not exist

## Created by
Created by Noah Smith and Arjun Esakkirajmohan