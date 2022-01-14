#############################################################################
# Program:
#    Lab PythonRPS_Server, Computer Networking
#    Brother Jones, CSE 354
# Author:
#    Jonathan Maxwell
# Summary:
#    This server program allows two clients to connect to it and enter
#    r, s, p, or q for a game of rock paper scissors
#
##############################################################################

import sys
from socket import *

# Check to make sure user has input a port number to use
# if wrong usage give error and exit
if len(sys.argv) == 2:
   port = int(sys.argv[1])
else:
   print('Wrong usage!')
   print('Example: python server.py \'port number\'')
   exit()

# Start the port running on given port
serverPort = 6789
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The Server is ready to receive')

try:
   while 1:
      # Connect two sockets
      connectionSocket1, addr1 = serverSocket.accept()
      connectionSocket2, addr2 = serverSocket.accept()

      # Receive usernames and send back to other client
      username1 = connectionSocket1.recv(1024).decode('ascii')
      username2 = connectionSocket2.recv(1024).decode('ascii')
      connectionSocket1.send(username2.encode('ascii'))
      connectionSocket2.send(username1.encode('ascii'))

      # What were the usernames
      print ('username 1: ', username1)
      print ('username 2: ', username2)

      # Receive whether or not connection is agreeable
      agreeable1 = connectionSocket1.recv(1024).decode('ascii')
      agreeable2 = connectionSocket2.recv(1024).decode('ascii')

      # If both is agreeable send back who was first and set is active to true
      if agreeable1 == 'y' and agreeable2 == 'y':
         # Who was first
         is_first = '1'
         is_not_first = '0'
         connectionSocket1.send(is_first.encode('ascii'))
         connectionSocket2.send(is_not_first.encode('ascii'))
         
         is_active = 1
      else:                # Otherwise return an n and set is active to false
         connectionSocket1.send('n'.encode('ascii'))
         connectionSocket2.send('n'.encode('ascii'))

         is_active = 0

      # As long as is_active is true begin chat service
      while is_active:

         # Receive message from first client and print
         message = connectionSocket1.recv(1024).decode('ascii')
         print ("Received from client1: ", message)

         # if message was q send to other client and break out of loop
         # otherwise send message to other client
         if message == 'q':
            connectionSocket2.send(message.encode('ascii'))
            break
         else:
            connectionSocket2.send(message.encode('ascii'))

         # Receive message from second client and print
         message = connectionSocket2.recv(1024).decode('ascii')
         print ("Received from client2: ", message)

         # if message was q send to other client and break out of loop
         # otherwise send message to other client
         if message == 'q':
            connectionSocket1.send(message.encode('ascii'))
            break
         else:
            connectionSocket1.send(message.encode('ascii'))

      # Make sure to close the Sockets after the loop and wait for two more
      connectionSocket1.close()
      connectionSocket2.close()
      print ('closed connections and looking for two more')

except KeyboardInterrupt:
   print("\nClosing Server")
   serverSocket.close()







