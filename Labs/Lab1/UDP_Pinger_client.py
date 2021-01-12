from socket import*
from datetime import datetime
import time

serverName='127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.connect((serverName, serverPort))
clientSocket.settimeout(1)
#print("Input Lowercase Sentence: ")
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

for message in test_pings:

    try:
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        initial_time = time.time()
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        ending_time = time.time()


        now = datetime.now()
        elapsed_time = str(ending_time - initial_time)
        #current_time = now.strftime("%H:%M:%S")
        print(modifiedMessage.decode(),
              now.strftime("%a"),
              now.strftime("%b"),
              now.strftime("%d"),
              now.strftime("%X"),
              now.strftime("%G"))
        print("RTT: ", elapsed_time)
    except timeout:
        print('Request Timed Out.')



clientSocket.close()