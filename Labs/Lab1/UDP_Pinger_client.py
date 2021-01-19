# Lab1, SYSC 4502
# Tanvir Hossain
# Student ID: 101058988

from socket import*
from datetime import datetime
import time
import sys

# Taking the arguments from Command line input
server_name = str(sys.argv[1])
server_port = int(sys.argv[2])

# Create socket Server
socket_client = socket(AF_INET, SOCK_DGRAM)
socket_client.connect((server_name, server_port))                          # Create a connection
socket_client.settimeout(1)                                                # Connection timeout set to 1 second

for ping_seq in range(1, 11):
    try:
        message = 'ping'                                             # Original message in lower case
        init_time = time.time()                                      # Taking the initial time stamp
        socket_client.sendto(message.encode(), (server_name, server_port))
        received_message, server_address = socket_client.recvfrom(2048)
        end_time = time.time()                                       # Taking the End time stamp
        current_date_time = datetime.now()                           # Taking the current date and time
        elapsed_time = str(end_time - init_time)                     # Subtracting the difference

        # Print all the required outputs
        # Formatters are used to printout data and time in required formats
        # mentioned in the lab handout
        print("Reply from", server_address[0], received_message.decode(), ping_seq,
              current_date_time.strftime("%a"),
              current_date_time.strftime("%b"),
              current_date_time.strftime("%d"),
              current_date_time.strftime("%X"),
              current_date_time.strftime("%G"))
        print("RTT: ", elapsed_time)
    except timeout:
        print('Request Timed Out.')

socket_client.close()
