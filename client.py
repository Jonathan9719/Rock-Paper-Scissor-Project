#############################################################################
# Program:
#    Final Project Chat Server, Computer Networking
#    Brother Jones, CSE 354
# Author:
#    Jonathan Maxwell
# Summary:
#    This client program allows the connection to a server where the user
#    can send messages back and forth with another client
#
##############################################################################

from socket import *
import sys

# Check to make sure the user has input a port and a server name
# if wrong usage give an error and exit
if len(sys.argv) == 3:
    serverName = str(sys.argv[1])
    serverPort = int(sys.argv[2])
else:
    print('Wrong usage!')
    print('Example: python client.py \'server name\' \'port number\'')
    exit()

# Create socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Check the port and hostname
try:
    clientSocket.connect(('localhost', 6789))
except gaierror as e:
    print('Bad hostname: ',   e)
    exit()
except error as e:
    print('Bad port number: ', e)
    exit()

# Get user's username and send to server
username = input('Please enter a username: ')
print('Please wait for connection. ')
clientSocket.send(username.encode('ascii'))

# Receive other user's username and print
otherUser = clientSocket.recv(1024).decode('ascii') 
print('You\'ve been connected with ', otherUser)

# If connection is agreeable continue otherwise exit the program
agreable = input('Would you like to conintue with connection(y) or cancel (n).')
clientSocket.send(agreable.encode('ascii'))
if agreable == 'n':
    print('Closing application')
    exit()

# Receive is first the three options are (1,0,n)
is_first = clientSocket.recv(1024).decode('ascii')

# If is_first is n then the other user didn't want to talk close program
if is_first == 'n':
    print(otherUser, ' did not want to talk. Closing application.')
    exit()

# set up message and reply
message = '0'
reply = '0'


while 1:

    # If is_first is true then prompt for message and receive reply
    # else reverse order and receive message then reply
    if is_first == '1':
        message = input('Input message or \'q\' to quit program: ')
        clientSocket.send(message.encode('ascii'))

        # Check if message was q and close otherwise continue
        if message == 'q':
            print('Closing connection. ')
            break
        else:
            # Receive reply and check if q and close otherwise continue and print
            reply = clientSocket.recv(1024).decode('ascii')
            if reply =='q':
                print('connection close by other person')
                break
            else:
                print('Reply: ', reply)
    else:
        # Check if message was q and close otherwise continue
        if message == 'q':
            print('Closing connection. ')
            break
        else:
            # Receive reply and check if q and close otherwise continue and print
            reply = clientSocket.recv(1024).decode('ascii')
            if reply =='q':
                print('connection close by other person')
                break
            else:
                print('Reply: ', reply)

        message = input('Input message or \'q\' to quit program: ')
        clientSocket.send(message.encode('ascii'))
else:
    clientSocket.close()


