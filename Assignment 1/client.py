from socket import*
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
    # keeps listening for user input until quit is typed in the command
    print("Client is Running. ")
    while 1:
        message = input("Input your command: \n")
        # If quit is typed, then both the server and client will quit
        if message == 'quit':
            try:
                socket_client.sendto(message.encode(), (server_name, server_port))
                received_message, server_address = socket_client.recvfrom(2048)     # Received msg from Server
                deserialized_message = pickle.loads(received_message)
                print(deserialized_message)
            except timeout:                                                         # Timer set to 1 second
                print('Request Timed Out.')
            print("User Requested to Quit. Quitting CLient ")
            exit()
        # For any other commands, it will be forwarded to server and processed there.
        else:
            try:
                socket_client.sendto(message.encode(), (server_name, server_port))
                received_message, server_address = socket_client.recvfrom(2048)
                deserialized_message = pickle.loads(received_message)
                print(deserialized_message)
            except timeout:
                print('Request Timed Out.')


socket_client.close()
