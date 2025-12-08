from socket import *
from threading import Thread
import sys
from typing import List
from ChatUI import ChatUI 
import message_protocol

serverName = "127.0.0.1" #or local host "127.0.0.1"#"192.168.1.2"#'hostname'#server's IP address (precisely IPv4)'servername'
serverPort = 12000 #un-reserved port #
clientSocket: socket
connectionOpen = False
chat: ChatUI
connected_users: List[str] = []

def handleServerMessages():
    global connectionOpen, chat, clientSocket
    while True:   #always listening for messages
        try:
            msg = message_protocol.recv_message(clientSocket)

            if not msg:
                clientSocket.close()  #connection closes
                print("\nServer disconnected")
                connectionOpen = False
                chat.destroy()
                break

            # print("Received", msg.decode())
            parts = msg.split('|', 2)

            if len(parts) < 2:
                continue

            messageType = parts[0]
            match messageType:
                case "GROUP":
                    sender = parts[1].strip()
                    message = parts[2] if len(parts) > 2 else ""
                    chat.add_message(message, username=sender)
                case "DIRECT":
                    sender = parts[1].strip()
                    message = parts[2] if len(parts) > 2 else ""
                    chat.add_message(message, username=sender)
                case "USERLIST":
                    user_string = parts[1]
                    connected_users = user_string.split(',') if user_string else []
                    print(f"Connected users: {', '.join(connected_users)}")
                case _:
                    continue
            
        except Exception as e:
            print(f"Connection error: {e}")
            connectionOpen = False
            chat.destroy()
            break

    clientSocket.close()

def send_message_to_server(message:str):
    global connectionOpen, clientSocket
    if not connectionOpen:
        print("Connection is closed, cannot send message")
        return
    # print("SENDING TO SERVER", message)
    try:        
        message_protocol.send_message(clientSocket, message)
    except KeyboardInterrupt:
        print("\nClient shutting down...")
        chat.destroy()



def main():
    global chat, clientSocket, connectionOpen
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM) #creates client side TCP socket
        clientSocket.connect((serverName,serverPort)) # initiates TCP connection
        connectionOpen = True
        localAddr = clientSocket.getsockname()
        print(f"Client connected from {localAddr[0]}:{localAddr[1]}")
        
        chat = ChatUI(send_message_to_server)
        t = Thread(target=handleServerMessages, daemon=True)
        t.start()

        chat.run()
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        connectionOpen = False
        if clientSocket:
            clientSocket.close()

if __name__ == "__main__":
    main()