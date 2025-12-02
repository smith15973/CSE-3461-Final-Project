from socket import *
from threading import Thread
import sys

serverName = "127.0.0.1" #or local host "127.0.0.1"#"192.168.1.2"#'hostname'#server's IP address (precisely IPv4)'servername'
serverPort = 12000 #un-reserved port #
connectionOpen = False

def handleServerMessages(clientSocket: socket):
    global connectionOpen
    while True:   #always listening for messages
        try:
            msg = clientSocket.recv(1024) #receives 'string' from server

            if not msg:
                clientSocket.close()  #connection closes
                print("\nServer disconnected")
                connectionOpen = False
                break

            print(msg.decode())
        except Exception as e:
            print(f"Connection error: {e}")
            connectionOpen = False
            break

    clientSocket.close()

def handleUserInput(clientSocket: socket):
    global connectionOpen
    connectionOpen = True
    try:
        while connectionOpen:
            sentence = input('Message:') #reads the string from client side user
            if not connectionOpen:
                break
            clientSocket.send(sentence.encode()) # this line encodes and sends the string 
    except KeyboardInterrupt:
        print("\nClient shutting down...")
    finally:
        clientSocket.close()



def main():
    clientSocket = socket(AF_INET, SOCK_STREAM) #creates client side TCP socket
    clientSocket.connect((serverName,serverPort)) # initiates TCP connection . After this line is executed, three-way handshake is performed and a TCP connection is established
    localAddr = clientSocket.getsockname()
    print(f"Client connected from {localAddr[0]}:{localAddr[1]}")

    t = Thread(target=handleServerMessages, args=(clientSocket,))
    t.start()

    input_t = Thread(target=handleUserInput, args=(clientSocket,))
    input_t.start()

    t.join()
    input_t.join()
    

if __name__ == "__main__":
    main()