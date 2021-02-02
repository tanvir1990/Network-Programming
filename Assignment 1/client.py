

from socket import*
from datetime import datetime
import time
import sys
import pickle

# Taking the arguments from Command line input
server_name = str(sys.argv[1])
server_port = int(sys.argv[2])

# server_name = "127.0.0.1"
# server_port = 12000

# Create socket Server
socket_client = socket(AF_INET, SOCK_DGRAM)
socket_client.settimeout(1)                                                # Connection timeout set to 1 second

for ping_seq in range(1, 2):

    while 1:
        message = input("Input your command: \n")

        if message == 'quit':
            try:
                socket_client.sendto(message.encode(), (server_name, server_port))
                received_message, server_address = socket_client.recvfrom(2048)
                deserialized = pickle.loads(received_message)
                print(deserialized)
            except timeout:
                print('Request Timed Out.')
            print("User Requested to Quit. Quitting CLient ")
            exit()
        else:
            try:
                socket_client.sendto(message.encode(), (server_name, server_port))
                received_message, server_address = socket_client.recvfrom(2048)
                deserialized = pickle.loads(received_message)
                print(deserialized)
            except timeout:
                print('Request Timed Out.')


socket_client.close()
