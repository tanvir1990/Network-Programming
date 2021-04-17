from socket import *
import sys
import struct
import os

def deletePid(delete_lines):
    with open("client_pid.txt", "r") as txt:
        lines = txt.readlines()
    with open("client_pid.txt", "w") as txt:
        for line in lines:
            if line.strip("\n") != delete_lines:
                txt.write(line)

def readTextfile(filename):
    result = ""
    try:
        f = open(filename)
    except:
        print("File ", filename, " does not exist")
        return ""
    for line in f:
        result = result + line
    return result


print("Client's PID is", os.getpid())
def createMessage(seq, msg, pid):
    return str(seq) + " " + msg + " " + str(pid)

def splitMessage(input):
    return (input[:input.find('@')], input[input.find('@')+1:])

# Get the server hostname and port as command line arguments
# argv = sys.argv
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
clientSocket.settimeout(3)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 1)
clientSocket.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, ttl)

# we will get a (potentially) large number of replies for each request
# add a sequence number to the messages and read replies until we get
# to the first one with a new sequence number

msg_sequence = 0
command_history = []

while True:
    file = open("client_pid.txt", "a+")
    file.write(str(os.getpid()) + '\n')
    file.close()
    msg_sequence += 1
    client_pid = os.getpid()
    message = createMessage(msg_sequence, input("Next command: "), client_pid)
    command = str(message.split()[1])

    if (len(command_history) == 2):
        command_history[0] = command_history[1]
        command_history.remove(command_history[1])


    if command == "quit":
        deletePid(str(os.getpid()))
        break
        exit(0)

    if command in command_history:
        print("Reply from Cache")
        read_cache = readTextfile("cache.txt")
        print(read_cache)

    else:
        command_history.append(command)
        try:
            clientSocket.sendto(message.encode(), (host, port))
            reply, serverAddress = clientSocket.recvfrom(2048)
            (seq, reply) = splitMessage(reply.decode())
            while int(seq) < msg_sequence:
                # print("Discard old reply")
                reply, serverAddress = clientSocket.recvfrom(2048)
                (seq, reply) = splitMessage(reply.decode())


            print(reply)
            # cache
            file = open("cache.txt", "w")
            file.write(reply)
            file.close()

            if reply == "bye":
                break
        except:
            print("Message to server timed out, please retry")


# once we break out of the loop, close socket and terminate
clientSocket.close()
