from socket import *
serverName = "127.0.0.1" #or local host "127.0.0.1"#"192.168.1.2"#'hostname'#server's IP address (precisely IPv4)'servername'
serverPort = 12000 #un-reserved port #
clientSocket = socket(AF_INET, SOCK_STREAM) #creates client side TCP socket
clientSocket.connect((serverName,serverPort)) # initiates TCP connection . After this line is executed, three-way handshake is performed and a 
# TCP connection is established

sentence = input('Input lowercase sentence:') #reads the string from client side user
clientSocket.send(sentence.encode()) # this line encodes and sends the string 

modifiedSentence = clientSocket.recv(1024) # the string is received here after getting modified from server. recv() method receives data from a socket and stores it in a buffer
print('From Server: ', modifiedSentence.decode()) # the string (now in UPPERCASE) is received from server, and  decoded.
clientSocket.close() # this closes the socket