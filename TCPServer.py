from socket import * 
import threading
serverPort = 12000 
clients: list[socket] = []

def broadcast(sender: socket, msg:str):
    for client in clients:
        if client is not sender:
                client.send(msg.encode())

def handleClientWork(connectionSocket: socket):
    while True:   #always listening for messages
        msg = connectionSocket.recv(1024).decode() #receives 'string' from client, and decodes it first

        if not msg:
            connectionSocket.close()  #connection closes
            clients.remove(connectionSocket)
            break

        broadcast(connectionSocket, msg)

def main():
    serverSocket = socket(AF_INET,SOCK_STREAM) #creating a server side socket
    serverSocket.bind(('',serverPort))  # bind() method associates a server socket with a specific address and port on the local machine
    serverSocket.listen(1) #this line means server listens for the TCP connection req. 
    print('The server is ready to receive')  # printing to confirm that TCP server is up and ready

    while True:   #always welcoming
        connectionSocket, addr = serverSocket.accept()  #create connection socket when client requests
        connectionSocket.send(f"Address: {addr[0]}, Port: {addr[1]}".encode()) #send client address and port info
        
        clients.append(connectionSocket) #add client socket to list of clients

        t = threading.Thread(target=handleClientWork, args=(connectionSocket,)) #create thread for client
        t.start() # start client thread

if __name__ == "__main__":
    main()