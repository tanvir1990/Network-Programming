# UDP_Pinger_Server.py 

# We will need the following module to generate randomized lost packets 

import random 
from socket import *
import pickle


# Create a UDP socket  
# Notice the use of SOCK_DGRAM for UDP packets 
serverSocket = socket(AF_INET, SOCK_DGRAM) 

# Assign IP address and port number to socket 
serverSocket.bind(('', 12000))

print("Server is running!")

def getDays():
	file_days = open("days.txt", 'r')
	dict_days = []
	for lines in file_days:
		dict_days.append(lines.strip())
	file_days.close()
	return dict_days

def getRooms():
	file_rooms = open("rooms.txt", 'r')
	dict_rooms = []
	for lines in file_rooms:
		dict_rooms.append(lines.strip())
	file_rooms.close()
	return dict_rooms

def getTime():
	file_time = open("timeslots.txt", 'r')
	dict_time = []
	for lines in file_time:
		dict_time.append(lines.strip())
	file_time.close()
	return dict_time

def check_reservation(room_number):
	file_reservation = open("reservations.txt", 'r')
	dict_reservation = []
	for lines in file_reservation:
		if lines.split()[0] == room_number:
			dict_reservation.append(lines.strip())
	file_reservation.close()
	return dict_reservation

def delete_a_reservation(delete_line):
	with open("reservations.txt", "r") as f:
		lines = f.readlines()
	with open("reservations.txt", "w") as f:
		for line in lines:
			if line.strip("\n") != delete_line:
				f.write(line)

def update_a_reservation(update_line):
	with open("reservations.txt", "a") as f:
		f.write( update_line + "\n")

while True:
	# Generate random number in the range of 0 to 9

	# Receive the client packet along with the address it is coming from 
	message_from_client, address = serverSocket.recvfrom(1024)

	if message_from_client.decode() == 'days':
		message_to_client = getDays()
		serialized = pickle.dumps(message_to_client)
		serverSocket.sendto(serialized,  address)

	if message_from_client.decode() == 'rooms':
		message_to_client = getRooms()
		serialized = pickle.dumps(message_to_client)
		serverSocket.sendto(serialized,  address)

	if message_from_client.decode() == 'timeslots':
		message_to_client = getTime()
		serialized = pickle.dumps(message_to_client)
		serverSocket.sendto(serialized,  address)

	if message_from_client.decode().split(' ')[0] == 'check':
		room_number = message_from_client.decode().split(' ')[1]
		message_to_client = check_reservation(room_number)
		serialized = pickle.dumps(message_to_client)
		serverSocket.sendto(serialized,  address)


	if message_from_client.decode().split(' ')[0] == 'delete':
		room_number = message_from_client.decode().split(' ')[1]
		timeSlot = message_from_client.decode().split(' ')[2]
		day = message_from_client.decode().split(' ')[3]

		delete_line = room_number + ' ' + timeSlot + ' ' + day
		delete_a_reservation(delete_line)

		message_to_client = " Deleted " + message_from_client.decode()
		serialized = pickle.dumps(message_to_client)
		serverSocket.sendto(serialized,  address)

	if message_from_client.decode().split(' ')[0] == 'reserve':
		room_number = message_from_client.decode().split(' ')[1]
		timeSlot = message_from_client.decode().split(' ')[2]
		day = message_from_client.decode().split(' ')[3]

		update_line = room_number + ' ' + timeSlot + ' ' + day
		update_a_reservation(update_line)

		message_to_client = " Reservation Successful!"
		serialized = pickle.dumps(message_to_client)
		serverSocket.sendto(serialized,  address)

	if message_from_client.decode().split(' ')[0] == 'quit':
		message_to_client = "Quitting Server"
		serialized = pickle.dumps(message_to_client)
		serverSocket.sendto(serialized,  address)
		print("User asked to Quit")
		exit()
