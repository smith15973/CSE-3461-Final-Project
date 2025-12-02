from socket import * 
serverPort = 12000 
serverSocket = socket(AF_INET,SOCK_STREAM) #creating a server side socket
serverSocket.bind(('',serverPort))  # bind() method associates a server socket with a specific address and port on the local machine
serverSocket.listen(1) #this line means server listens for the TCP connection req. 
print('The server is ready to receive')  # printing to confirm that TCP server is up and ready
while True:   #always welcoming
    connectionSocket, addr = serverSocket.accept()  #When a client knocks on this door, the program invokes the  method for serverSocket, 
    #which creates a new socket in the server, called , dedicated to this particular client.

    sentence = connectionSocket.recv(1024).decode() #receives 'string' from client, and decodes it first

    capitalizedSentence = sentence.upper()    #converts to an UPPERCASE

    connectionSocket.send(capitalizedSentence.encode()) # sends back to the client
    connectionSocket.close()  #connection closes