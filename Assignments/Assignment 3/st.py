from socket import *
import sys
import threading
import random
import time
import struct
import os
from subprocess import check_output
from os import path

# read in information one textfile, store and return as one long string



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

# write reservations textfile
def writeTextfile(filename, input):
    try:
        f = open(filename, "w")
    except:
        print("File ", filename, " could not be opened for writing")
        return
    for line in input:
        f.write(line + "\n")

# check format of RESERVE and DELETE commands
def checkFormat(cmd_components):
    # check for sufficient fields
    if len(cmd_components) != 4:
        return "Inaccurate number of parameters"
    # check for valid input fields
    if cmd_components[1] not in rooms:
        return cmd_components[1] + " not a valid room"
    if cmd_components[2] not in timeslots:
        return cmd_components[2] + " not a valid timeslot"
    if cmd_components[3] not in days:
        return cmd_components[3] + " not a valid day"
    # if we are here, everything worked out, return okay
    return "okay"

# process a single user command, returning either the result or an appropriate error message
def processCommand(cmd):
    global res
    if cmd == "days":
        return days
    if cmd == "rooms":
        return rooms
    if cmd == "timeslots":
        return timeslots
    if cmd[:5] == "check":
        specific_room = cmd[6:]
        if specific_room not in rooms:
            return "Room " + specific_room + " not a valid room"
        results = ""
        for r in res:
            components = r.split()
            if components[0] == specific_room:
                if not results == "":
                    results = results + "\n"
                results = results + r 
        if results == "":
            results = "No room reservation found"
        return results
    if cmd[:7] == "reserve":
        cmd_components = cmd.split()
        check_results = checkFormat(cmd_components)
        if not check_results == "okay":
            return check_results

	# check whether reservation already exists
        found = False
        for r in res:
            components = r.split()
            if components[0] == cmd_components[1] and components[1] == cmd_components[2] and components[2] == cmd_components[3]:
                found = True
        if found:
            return "Reservation already exists"
        
        # once we are here, add reservation and return confirmation
        new_res = cmd_components[1] + " " + cmd_components[2] + " " + cmd_components[3]
        res.append(new_res)
        # save new reservations in textfile (i.e., stable storage)
        writeTextfile("reservations.txt", res)
        return "Reservation confirmed"
    if cmd[:6] == "delete":
        cmd_components = cmd.split()
        check_results = checkFormat(cmd_components)
        if not check_results == "okay":
            return check_results

        # iterate over all reservations, copy all the ones that are not involved to new_reservations
        found = False
        new_res = []
        for r in res:
            components = r.split()
            if components[0] == cmd_components[1] and components[1] == cmd_components[2] and components[2] == cmd_components[3]:
                found = True
            else:
                new_res.append(r)
        if not found:
            return "Reservation did not exist"

        # we had a proper deletion request, store this as the new set and return a deletion confirmation
        res = new_res
       # save new reservations in textfile (i.e., stable storage)
        writeTextfile("reservations.txt", res)
        return "Deletion confirmed"
    if cmd == "quit":
        return "bye"
    # if we get here, the command is unknown, simply return error message
    return cmd + ": Command unknown"

# helper functions to create messages and to split messages

def createMessage(seq, msg):
    return str(seq) + "@" + msg

def splitMessage(input):
    return (input[:input.find('@')], input[input.find('@')+1:])

# create Threading class - one instance per launched threat, dealing with one user command

def get_pid(name):
    return check_output(["pidof", name]).decode().split()


# Function that checks if a server is leader


def parsing():
    file = open("All_pids.txt", "w")
    tasklist = check_output("tasklist | findstr python.exe", shell=True).decode()
    file.write(tasklist)
    file.close()

    # Previous Gives empty line after each line
    # So the following operation gets rid of the new empty lines
    with open('All_pids.txt') as infile, open('All_pids_cleaned.txt', 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output
    infile.close()
    outfile.close()

    # remove server_pid.txt
    # if path.exists("All_pids.txt"):
    #     os.remove('All_pids.txt')


    file = open("All_pids_cleaned.txt", "r+")
    tasklist_lines = file.readlines()
    All_pids = []
    for line in tasklist_lines:
        if line is not []:
            a,server_pid,c,d,e,f = line.split()
            All_pids.append(int(server_pid))
    file.close()

    # if path.exists("All_pids_cleaned.txt"):
    #     os.remove('All_pids_cleaned.txt')

    print("All PIDs", All_pids)
    # Find the highest of the PIDs

    # read from client_pid.txt, tanvir_pid is client PID
    file = open("client_pid.txt", "r+")
    client_pid_lines = file.readlines()
    for client_pid in client_pid_lines:
        if int(client_pid.strip()) in All_pids:
            All_pids.remove(int(client_pid.strip()))

    file.close()
    only_server_pids = All_pids

    print("After removing the client Pids", only_server_pids)

    #
    file = open("highest_server_pid.txt", "w")
    highest_server_pid = max(only_server_pids)
    # if os.getpid() != highest_server_pid:
    file.write(str(highest_server_pid))
    file.close()



def isLeader():
    max_pid = readTextfile("highest_server_pid.txt")
    print ("Max_pid", max_pid)

    if os.getpid() == int(max_pid.strip()):
        print("I AM THE LEADER")
        return True
    else:
        return False




threadLock = threading.Lock()
class ClientCmdThread(threading.Thread):

    def __init__(self, ip, port, msg):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port

        # Message also contains Client's PID, just in case
        message = msg.decode()
        (self.sequence_number, self.msg, client_pid) = message.split()


    def run(self):
        print("The Server Process ID ", os.getpid())
        parsing()
        print("Start executing thread for:", self.msg, "with sequence number", self.sequence_number)
        answer = createMessage(self.sequence_number, processCommand(self.msg))
        process_Id = os.getpid()
        #threadLock.acquire()
        result = isLeader()
        if result == True:
            print("Server with Process Id", os.getpid(), " is the Leader")
            serverSocket.sendto(answer.encode(), (self.ip, self.port))
	        # Generate random number in the range of 2 to 4 and sleep
            rand = random.randint(5, 10)
            time.sleep(rand)
            print("End executing thread for:", self.msg)
        else:
            print("Server Process", os.getpid(), "IS NOT THE LEADER. SO IT's NOT SENDING ANY REPLY TO CLIENT. ")
        #threadLock.release()


# Get the multicast group address and server port as command line arguments and set up the server socket
argv = sys.argv                      
# if len(argv ) != 3:
#     print("Incorrect number of command-line arguments")
#     print("Invoke server with: python", argv[0], "<MulticastIP> <port>")
#     exit()

# multicastGroup = argv[1]
# serverPort = int(argv[2])

multicastGroup = '224.3.29.71'
serverPort = 10000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# allow multiple server/receiver processes on the same computer to bind to the multicast port
#
# IMPORTANT
#
# Windows does not support SO_REUSEPORT, so we need to use REUSEADDR
#
# Linux/MacOS: need to use REUSEPORT
#
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# Bind to the server address: localhost and serverPort
serverSocket.bind(('', serverPort))

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = inet_aton(multicastGroup)
mreq = struct.pack('4sL', group, INADDR_ANY)
serverSocket.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)

# read in the information in the four input textfiles
rooms = readTextfile("rooms.txt")
days = readTextfile("days.txt")
timeslots = readTextfile("timeslots.txt")
reservations = readTextfile("reservations.txt")
# split reservations into a list for easier handling later
res = reservations.splitlines()

print ("The server is ready to receive")

# main server loop: receive a single datagram with a message/command and act on it
while True:
    message, (clientIP, clientPort) = serverSocket.recvfrom(2048)
    newClientThread = ClientCmdThread(clientIP, clientPort, message)
    newClientThread.start()


# once we break out of the loop, close socket and terminate
serverSocket.close()
print ("Shutting the server down")
