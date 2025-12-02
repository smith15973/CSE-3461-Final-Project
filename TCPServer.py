from socket import * 
import threading
serverPort = 12000 
clients: list[socket] = []
clients_lock = threading.Lock()

def remove_client(client:socket):
    with clients_lock:
        if client in clients:  # avoid KeyError
            clients.remove(client)

def broadcast(sender: socket, msg:str):
    with clients_lock: 
        clients_copy = list(clients)
    for client in clients_copy:
        if client is sender:
                continue
        try:
            client.send(msg.encode())
        except OSError:
            # socket is dead → remove it safely
            remove_client(client)
            client.close()

def handleClientWork(connectionSocket: socket):
    while True:   #always listening for messages
        msg = connectionSocket.recv(1024) #receives 'string' from client

        if not msg:
            connectionSocket.close()  #connection closes
            remove_client(connectionSocket)
            break

        broadcast(connectionSocket, msg.decode())

def main():
    serverSocket = socket(AF_INET,SOCK_STREAM) #creating a server side socket
    serverSocket.bind(('',serverPort))  # bind() method associates a server socket with a specific address and port on the local machine
    serverSocket.listen() #this line means server listens for the TCP connection req. 
    print('The server is ready to receive')  # printing to confirm that TCP server is up and ready

    while True:   #always welcoming
        connectionSocket, addr = serverSocket.accept()  #create connection socket when client requests
        connectionSocket.send(f"Address: {addr[0]}, Port: {addr[1]}".encode()) #send client address and port info
        
        with clients_lock:
            clients.append(connectionSocket) #add client socket to list of clients

        t = threading.Thread(target=handleClientWork, args=(connectionSocket,)) #create thread for client
        t.start() # start client thread

if __name__ == "__main__":
    main()