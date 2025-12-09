from socket import *
from threading import Thread
import sys
from typing import List
from ChatUI import ChatUI 
import message_protocol

serverName = "127.0.0.1"  # Default to localhost
serverPort = 12000
clientSocket: socket = None
connectionOpen = False
chat: ChatUI = None
username: str = None
connected_users: List[str] = []

def handleServerMessages():
    """Background thread to continuously receive messages from server"""
    global connectionOpen, chat, clientSocket
    
    while connectionOpen:
        try:
            msg = message_protocol.recv_message(clientSocket)

            if not msg:
                # Server disconnected
                print("\nServer disconnected")
                connectionOpen = False
                if chat:
                    chat.destroy()
                break

            # Parse message format: TYPE|SENDER|MESSAGE
            parts = msg.split('|', 2)

            if len(parts) < 2:
                continue

            messageType = parts[0]
            
            if messageType == "GROUP":
                # Broadcast message: GROUP|sender|message
                sender = parts[1].strip()
                message = parts[2] if len(parts) > 2 else ""
                chat.add_message(message, username=sender, isReceived=True)
                
            elif messageType == "DIRECT":
                # Direct message: DIRECT|sender|message
                sender = parts[1].strip()
                message = parts[2] if len(parts) > 2 else ""
                chat.add_message(f"[Private] {message}", username=sender, isReceived=True)
                
            elif messageType == "USERLIST":
                # User list update: USERLIST|user1,user2,user3
                user_string = parts[1]
                connected_users = [u.strip() for u in user_string.split(',') if u.strip()]
                print(f"\nConnected users: {', '.join(connected_users)}")
                
            elif messageType == "SYSTEM":
                # System message: SYSTEM||message
                message = parts[2] if len(parts) > 2 else parts[1]
                chat.add_message(message, username="System", isReceived=True)
                
            elif messageType == "ERROR":
                # Error message: ERROR||message
                message = parts[2] if len(parts) > 2 else parts[1]
                chat.add_message(f"⚠️ {message}", username="Error", isReceived=True)
            
        except Exception as e:
            if connectionOpen:
                print(f"Connection error: {e}")
                connectionOpen = False
                if chat:
                    chat.destroy()
            break

    # Clean up
    try:
        if clientSocket:
            clientSocket.close()
    except:
        pass

def send_message_to_server(message: str):
    """Send a message to the server"""
    global connectionOpen, clientSocket
    
    if not connectionOpen:
        print("Connection is closed, cannot send message")
        return
    
    if not message.strip():
        return
    
    try:
        message_protocol.send_message(clientSocket, message)
    except Exception as e:
        print(f"Error sending message: {e}")
        connectionOpen = False
        if chat:
            chat.destroy()

def main():
    global chat, clientSocket, connectionOpen, username

    print("=== TCP Chat Client ===")
    
    # Get server connection info
    server_input = input(f"Enter server address (default {serverName}): ").strip()
    server = server_input if server_input else serverName
    
    port_input = input(f"Enter server port (default {serverPort}): ").strip()
    port = int(port_input) if port_input else serverPort
    
    # Get username from user
    username = input("Enter your username: ").strip()
    if not username:
        print("Username cannot be empty")
        return
    
    try:
        # Create and connect socket
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((server, port))
        connectionOpen = True

        # Get local address info
        localAddr = clientSocket.getsockname()
        full_username = f"{username} ({localAddr[0]}:{localAddr[1]})"

        # Send username to server
        message_protocol.send_message(clientSocket, f"USERNAME|{full_username}")
        print(f"Connected to {server}:{port} as '{full_username}'")
        print("\nInstructions:")
        print("  - Type normally to send broadcast messages to all users")
        print("  - Type @username message to send a direct message")
        print("  - Type /users to see connected users")
        print("\nOpening chat window...")
        
        # Create GUI
        chat = ChatUI(send_message_to_server, width=500, height=600)
        
        # Start background thread to receive messages
        t = Thread(target=handleServerMessages, daemon=True)
        t.start()

        # Run GUI (blocking call)
        chat.run()
        
    except ConnectionRefusedError:
        print(f"Error: Could not connect to server at {server}:{port}")
        print("Make sure the server is running first!")
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        connectionOpen = False
        if clientSocket:
            try:
                clientSocket.close()
            except:
                pass
        print("Client closed.")

if __name__ == "__main__":
    main()