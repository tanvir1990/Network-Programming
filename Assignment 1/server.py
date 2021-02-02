# SYSC 4502 Assignment 1
# Tanvir Hossain
# 101058988

# Built on Lab1
import random
from socket import *
import pickle

# Create a UDP socket  
serverSocket = socket(AF_INET, SOCK_DGRAM) 						# Notice the use of SOCK_DGRAM for UDP packets
serverSocket.bind(('', 12000))									# Assign IP address and port number to socket
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


def addReservation(message_from_client, address):
	message = message_from_client.decode()
	reservation_exists = False
	room_number = message.split(' ')[1]
	timeSlot = message.split(' ')[2]
	day = message.split(' ')[3]

	reserve_information_from_client = room_number + ' ' + timeSlot + ' ' + day
	file = open("reservations.txt", "r+")
	lines = file.readlines()
	# Check if the reservation already exists
	for line in lines:
		if reserve_information_from_client.strip() == line.strip():
			reservation_exists = True
			break
	if reservation_exists == True:
		message_to_client = "Error: Reservation already Exists"
		send_message_to_client(message_to_client, address)
	else:
		file.write(reserve_information_from_client + "\n")
		message_to_client = " Reservation Successful!"
		send_message_to_client(message_to_client, address)
	file.close()


def send_message_to_client(message, address):
	serialized = pickle.dumps(message)
	serverSocket.sendto(serialized, address)


while True:
	# Receive the client packet along with the address it is coming from
	message_from_client, address = serverSocket.recvfrom(1024)

	if message_from_client.decode() == 'days':
		message_to_client = getDays()
		send_message_to_client(message_to_client, address)

	elif message_from_client.decode() == 'rooms':
		message_to_client = getRooms()
		send_message_to_client(message_to_client, address)

	elif message_from_client.decode() == 'timeslots':
		message_to_client = getTime()
		send_message_to_client(message_to_client, address)

	elif message_from_client.decode().split(' ')[0] == 'check':
		room_number = message_from_client.decode().split(' ')[1]
		message_to_client = check_reservation(room_number)
		send_message_to_client(message_to_client, address)

	elif message_from_client.decode().split(' ')[0] == 'delete':
		room_number = message_from_client.decode().split(' ')[1]
		timeSlot = message_from_client.decode().split(' ')[2]
		day = message_from_client.decode().split(' ')[3]

		delete_line = room_number + ' ' + timeSlot + ' ' + day
		delete_a_reservation(delete_line)

		message_to_client = " Deleted " + message_from_client.decode()
		send_message_to_client(message_to_client, address)

	elif message_from_client.decode().split(' ')[0] == 'reserve':
		addReservation(message_from_client, address)

	elif message_from_client.decode().split(' ')[0] == 'quit':
		message_to_client = "User Requested to Quit. Shutting down server"
		serialized = pickle.dumps(message_to_client)
		serverSocket.sendto(serialized,  address)
		print("User requested to Quit. Quitting Server")
		exit()

	else:
		message_to_client = "ERROR: Server Received Invalid command"
		serialized = pickle.dumps(message_to_client)
		serverSocket.sendto(serialized,  address)
