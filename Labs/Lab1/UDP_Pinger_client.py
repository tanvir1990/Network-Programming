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
socket_client.settimeout(1)                                              # Connection timeout set to 1s

# Creating 10 Ping Messages into an array of String messages
# It could have been done inside the for loop as well
# but I found this way it's easier
test_pings = ['ping 1',
              'ping 2',
              'ping 3',
              'ping 4',
              'ping 5',
              'ping 6',
              'ping 7',
              'ping 8',
              'ping 9',
              'ping 10']
# Using a For loop, going through the Array of messages for 10 times
for message in test_pings:
    try:
        socket_client.sendto(message.encode(), (server_name, server_port))
        init_time = time.time()                                      # Taking the initial time stamp
        modifiedMessage, server_address = socket_client.recvfrom(2048)
        end_time = time.time()                                       # Taking the End time stamp
        current_date_time = datetime.now()                                            # Taking the current date and time
        elapsed_time = str(end_time - init_time)                  # Subtracting the difference

        # Print all the required outputs
        # Formatters are used to printout data and time in required formats
        # mentioned in the lab handout
        print("Reply from", server_address[0], modifiedMessage.decode(),
              current_date_time.strftime("%a"),
              current_date_time.strftime("%b"),
              current_date_time.strftime("%d"),
              current_date_time.strftime("%X"),
              current_date_time.strftime("%G"))
        print("RTT: ", elapsed_time)
    except timeout:
        print('Request Timed Out.')

socket_client.close()
