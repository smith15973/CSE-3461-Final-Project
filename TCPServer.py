from socket import * 
import threading
import message_protocol

serverPort = 12000 
clients: dict[socket, str] = {}  # socket -> username mapping
clients_lock = threading.Lock()

def broadcast_connected_users():
    """Send list of all connected users to all clients"""
    with clients_lock: 
        clients_copy = dict(clients)
    # Create comma-separated list of usernames
    clients_string = ','.join(username for username in clients_copy.values())
    broadcast(f"USERLIST|{clients_string}")

def remove_client(client: socket):
    """Remove a client from the active clients dictionary"""
    with clients_lock:
        if client in clients:
            username = clients.pop(client)
            print(f"{username} disconnected")
    broadcast_connected_users()

def broadcast(msg: str, sender: socket = None):
    """Send a message to all connected clients except the sender"""
    with clients_lock: 
        clients_copy = dict(clients)
    
    for client in clients_copy.keys():
        if client is sender:
            continue
        try:
            message_protocol.send_message(client, msg)
        except OSError:
            # Socket is dead, remove it
            remove_client(client)
            try:
                client.close()
            except:
                pass

def send_direct_message(sender_socket: socket, target_username: str, message: str):
    """Send a direct message to a specific user"""
    sender_username = clients.get(sender_socket, "Unknown")
    
    # Find the target client socket
    target_socket = None
    with clients_lock:
        for sock, username in clients.items():
            if username == target_username:
                target_socket = sock
                break
    
    if target_socket:
        try:
            # Send to target
            message_protocol.send_message(
                target_socket, 
                f"DIRECT|{sender_username}|{message}"
            )
            # Send confirmation back to sender
            message_protocol.send_message(
                sender_socket,
                f"SYSTEM||Message sent to {target_username}"
            )
        except OSError:
            # Target socket is dead
            remove_client(target_socket)
            message_protocol.send_message(
                sender_socket,
                f"ERROR||User {target_username} is no longer connected"
            )
    else:
        # User not found
        message_protocol.send_message(
            sender_socket,
            f"ERROR||User '{target_username}' not found. Use /users to see connected users."
        )

def handleClientWork(connectionSocket: socket):
    """Handle communication with a single client"""
    username = None
    
    # Get the username from the client
    try:
        message = message_protocol.recv_message(connectionSocket)

        if message is None:
            print("Connection closed during setup")
            connectionSocket.close()
            return

        # Validate message format: USERNAME|username
        parts = message.split('|')
        if len(parts) != 2 or parts[0] != "USERNAME" or not parts[1]:
            print("Invalid username format")
            connectionSocket.close()
            return

        # Remove illegal characters from username
        username = parts[1].replace(',', '').replace('|', '')
    
        # Add client to dictionary
        with clients_lock:
            clients[connectionSocket] = username
        
        print(f"{username} connected")
        
        # Send updated user list to all clients
        broadcast_connected_users()
        
        # Send welcome message to the new client
        message_protocol.send_message(
            connectionSocket,
            "SYSTEM||Welcome! Type /users to see connected users. Use @username message for direct messages."
        )
        
    except Exception as e:
        print(f"Error during client setup: {e}")
        connectionSocket.close()
        return

    # Main message loop
    while True:
        try:
            data = message_protocol.recv_message(connectionSocket)

            if not data:
                # Client disconnected
                connectionSocket.close()
                remove_client(connectionSocket)
                break
            
            # Check for commands
            if data.startswith('/users'):
                # Send list of connected users
                broadcast_connected_users()
                continue
            
            # Check for direct message format: @username message
            if data.startswith('@'):
                # Parse the direct message
                parts = data[1:].split(' ', 1)
                if len(parts) < 2:
                    message_protocol.send_message(
                        connectionSocket,
                        "ERROR||Invalid format. Use: @username message"
                    )
                    continue
                
                target_username = parts[0].strip()
                message_text = parts[1].strip()
                
                if not target_username or not message_text:
                    message_protocol.send_message(
                        connectionSocket,
                        "ERROR||Invalid format. Use: @username message"
                    )
                    continue
                
                # Send direct message
                send_direct_message(connectionSocket, target_username, message_text)
            else:
                # Regular broadcast message
                msg = f"GROUP|{username}|{data}"
                broadcast(msg, sender=connectionSocket)
                
        except Exception as e:
            print(f"Error handling client {username}: {e}")
            connectionSocket.close()
            remove_client(connectionSocket)
            break

def main():
    # Get port from user
    port_input = input(f"Enter port number to start server on (default {serverPort}): ").strip()
    port = int(port_input) if port_input else serverPort

    serverSocket = socket(AF_INET, SOCK_STREAM)
    
    # Allow address reuse (helpful for quick restarts)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    serverSocket.bind(('', port))
    serverSocket.listen()
    
    print(f'Server is ready to receive on port {port}')
    print("Press Ctrl+C to stop the server")

    try:
        while True:
            connectionSocket, addr = serverSocket.accept()
            print(f"New connection from {addr}")

            # Create and start thread for this client
            t = threading.Thread(target=handleClientWork, args=(connectionSocket,), daemon=True)
            t.start()

    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        serverSocket.close()

if __name__ == "__main__":
    main()