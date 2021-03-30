from socket import *
import sys
import struct

# helper functions to create messages and to split messages

def createMessage(seq, msg, pid):
    return str(seq) + " " + msg + " " + str(pid)

def splitMessage(input):
    return (input[:input.find('@')], input[input.find('@')+1:])

# Get the server hostname and port as command line arguments
argv = sys.argv                      
# if len(argv ) != 3:
#     print("Incorrect number of command-line arguments")
#     print("Invoke client with: python", argv[0], "<MulticastIP> <port>")
#     exit()

# host = argv[1]
# port = int(argv[2])

host = '224.3.29.71'
port = 10000



clientSocket = socket(AF_INET, SOCK_DGRAM)
# Set socket timeout as 1 second
clientSocket.settimeout(1)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 1)
clientSocket.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, ttl)

# we will get a (potentially) large number of replies for each request
# add a sequence number to the messages and read replies until we get
# to the first one with a new sequence number

msg_sequence = 0

while True:

    msg_sequence += 1
    client_pid = 123456
    message = createMessage(msg_sequence, input("Next command: "), client_pid)
    
    try:
        clientSocket.sendto(message.encode(), (host, port))
        reply, serverAddress = clientSocket.recvfrom(2048)
        (seq, reply) = splitMessage(reply.decode())
        while int(seq) < msg_sequence:
            # print("Discard old reply")
            reply, serverAddress = clientSocket.recvfrom(2048)
            (seq, reply) = splitMessage(reply.decode())

        print(reply)
        if reply == "bye":
            break
    except:
        print("Message to server timed out, please retry")

# once we break out of the loop, close socket and terminate
clientSocket.close()
