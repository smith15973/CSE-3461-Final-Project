from socket import *
from threading import Thread

serverName = "127.0.0.1" #or local host "127.0.0.1"#"192.168.1.2"#'hostname'#server's IP address (precisely IPv4)'servername'
serverPort = 12000 #un-reserved port #
connectionOpen = False

def handleServerMessages(clientSocket: socket):
    while True:   #always listening for messages
        msg = clientSocket.recv(1024).decode() #receives 'string' from server, and decodes it first

        print('From Server:', msg)

        if not msg:
            clientSocket.close()  #connection closes
            print("Server shutdown")
            global connectionOpen
            connectionOpen = False
            break

def main():
    clientSocket = socket(AF_INET, SOCK_STREAM) #creates client side TCP socket
    clientSocket.connect((serverName,serverPort)) # initiates TCP connection . After this line is executed, three-way handshake is performed and a TCP connection is established
    addressInfo = clientSocket.recv(1024).decode() #receives 'string' from server, and decodes it first
    print(addressInfo)
    t = Thread(target=handleServerMessages, args=(clientSocket,))
    t.start()
    global connectionOpen
    connectionOpen = True
    while connectionOpen:
        sentence = input('Message:') #reads the string from client side user
        clientSocket.send(sentence.encode()) # this line encodes and sends the string 

if __name__ == "__main__":
    main()