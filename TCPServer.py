from socket import * 
import threading
import message_protocol
serverPort = 12000 
clients: dict[socket, str] = {}
clients_lock = threading.Lock()

def broadcast_connected_users():
    with clients_lock: 
        clients_copy = dict(clients)
    clients_string = ', '.join(f"{username}" for username in clients_copy.values())
    broadcast(f"USERLIST|{clients_string}")

def remove_client(client:socket):
    with clients_lock:
        if client in clients:  # avoid KeyError
            username = clients.pop(client)
            print(f"{username} disconnected")
    broadcast_connected_users()

def broadcast(msg:str, sender: socket = None,):
    with clients_lock: 
        clients_copy = dict(clients)
    for client in clients_copy.keys():
        if client is sender:
                continue
        try:
            message_protocol.send_message(client, msg)
        except OSError:
            # socket is dead → remove it safely
            remove_client(client)
            client.close()

def handleClientWork(connectionSocket: socket):
    username = None
    # get the username from the client and save it to the server
    try:
        message = message_protocol.recv_message(connectionSocket)

        # Handle connection closed
        if message is None:
            print("Connection closed")
            connectionSocket.close()
            return  # or continue, depending on your loop structure

        # Validate message format
        parts = message.split('|')
        if len(parts) != 2 or parts[0] != "USERNAME" or not parts[1]:
            connectionSocket.close()
            return

        username = parts[1].replace(',', '') #remove illegal comma characters for splicing
    
        # Add client to dictionary
        with clients_lock:
            clients[connectionSocket] = username
        
        print(f"{username} connected")
        
        # Send updated user list to all clients
        broadcast_connected_users()
        
    except Exception as e:
        print(f"Error during client setup: {e}")
        connectionSocket.close()
        return

    while True:   #always listening for messages
        data = message_protocol.recv_message(connectionSocket)

        if not data:
            connectionSocket.close()
            remove_client(connectionSocket)
            break
        msg = f"GROUP|{username}|{data}"
        broadcast(msg, sender=connectionSocket)

def main():
    # Get port from user
    port_input = input("Enter port number to start server on (default 12000): ").strip()
    port = int(port_input) if port_input else serverPort

    serverSocket = socket(AF_INET,SOCK_STREAM) #creating a server side socket
    serverSocket.bind(('', port))  # bind() method associates a server socket with a specific address and port on the local machine
    serverSocket.listen() #this line means server listens for the TCP connection req. 
    
    print(f'Server is ready to receive on port {port}')

    while True:   #always welcoming
        try:
            connectionSocket, addr = serverSocket.accept()  #create connection socket when client requests

            t = threading.Thread(target=handleClientWork, args=(connectionSocket,)) #create thread for client
            t.start() # start client thread

        except KeyboardInterrupt:
            print("\nShutting down Server")
            break

if __name__ == "__main__":
    main()