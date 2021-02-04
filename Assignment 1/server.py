
# Built on Lab1
import random
from socket import *
import pickle
import sys

# Create a UDP socket  
serverSocket = socket(AF_INET, SOCK_DGRAM)
server_port = int(sys.argv[1])
serverSocket.bind(('', server_port))							# Assign IP address and port number to socket
print("Server is running!")


def get_days():
	"""get_days returns the list of days from days.txt

	:parameter
	none
	:return
	a list of days
	"""
	file_days = open("days.txt", 'r')
	days = []
	for lines in file_days:
		days.append(lines.strip())
	file_days.close()
	return days


def get_rooms():
	"""get_rooms() returns the list of rooms from rooms.txt

	:parameter
	none
	:return
	a list of rooms
	"""
	file_rooms = open("rooms.txt", 'r')
	dict_rooms = []
	for lines in file_rooms:
		dict_rooms.append(lines.strip())
	file_rooms.close()
	return dict_rooms


def getTime():
	"""get_time() returns all the slots that are mentioned
	in timeslots.txt

	:parameter
	none
	:return:
	a list of timeslots
	"""
	file_time = open("timeslots.txt", 'r')
	dict_time = []
	for lines in file_time:
		dict_time.append(lines.strip())
	file_time.close()
	return dict_time


def check_reservation(room_number):
	"""this function returns the existing reservation from
	reservation.txt

	:parameter
	room number that user requested for
	:return
	a list of all existing reservations"""
	file_reservation = open("reservations.txt", 'r')
	lines = file_reservation.readlines()
	reservations = []
	for lines in lines:
		if lines.split(' ')[0] == room_number:
			reservations.append(lines.strip())
	file_reservation.close()
	return reservations


def delete_a_reservation(message_from_client, address):
	"""deletes a reservation from the reservations.txt and then
	sends confirmation to client

	:param message_from_client: user request
	:param address: client address
	:return:
	"""
	# Splitting the message to extract the following information
	room_number = message_from_client.decode().split(' ')[1]
	timeSlot = message_from_client.decode().split(' ')[2]
	day = message_from_client.decode().split(' ')[3]

	delete_reservation = room_number + ' ' + timeSlot + ' ' + day		# Delete line is reservation that needs to be deleted

	# First we need to check if the requests are valid or according the format
	if (is_timeslots_valid(message_from_client, address) is False or
			is_day_valid(message_from_client, address) is False or
			is_room_valid(message_from_client, address) is False):
		print("Invalid input for either day, time or room. \n Look at messages at client side")
	# if the requests are valid then delete the reservation
	else:
		if reservation_exists_for(delete_reservation):
			with open("reservations.txt", "r") as f:
				lines = f.readlines()
			with open("reservations.txt", "w") as f:
				for line in lines:
					if line.strip("\n") != delete_reservation:
						f.write(line)

			message_to_client = " Deleted the reservation for " + delete_reservation
			send_message_to_client(message_to_client, address)
		else:
			message_to_client = " Reservation Does not exist for " + delete_reservation
			send_message_to_client(message_to_client, address)


def reservation_exists_for(message):
	"""checks if a reservation exists before adding or deleting a reservation

	:parameter
	client's message or request
	:return
	True if the reservation exists. otherwise, return false"""
	file = open("reservations.txt", "r+")
	lines = file.readlines()
	for line in lines:
		if message.strip() == line.strip():
			return True
			break
	file.close()


def add_reservation(message_from_client, address):
	"""adds a reservation to reservation.txt. The update in the reservations.txt
	can only be seen after the server is closed. It also depends on the oS or what application is being used to
	read reservations.txt. Upon successful addition of reservation, it sends a confirmation to client.

	:param message_from_client: user request
	:param address: client's address
	:return:
	"""
	# Checks if the requests are valid or according the format
	if (is_timeslots_valid(message_from_client, address) is False or
		is_day_valid(message_from_client, address) is False or
		is_room_valid(message_from_client, address) is False):
		print("Invalid input for either day, time or room. \n Look at messages at client side")
	# If the requests are valid add the reservation
	else:
		message = message_from_client.decode()
		reservation_exists = False
		room_number = message.split(' ')[1]
		timeSlot = message.split(' ')[2]
		day = message.split(' ')[3]

		reserve_information_from_client = room_number + ' ' + timeSlot + ' ' + day
		# Before adding the reservation, checks if the reservation exists
		# for the information that is provided by client
		if reservation_exists_for(reserve_information_from_client):
			message_to_client = "Error: Reservation already Exists"
			send_message_to_client(message_to_client, address)
		else:
			file = open("reservations.txt", "a+")
			file.write(reserve_information_from_client + "\n")
			message_to_client = " Reservation Successful!"
			send_message_to_client(message_to_client, address)
			file.close()


def send_message_to_client(message, address):
	"""general function to handle sending operation

	:param message:
	:param address: client address
	:return:
	"""
	serialized = pickle.dumps(message)
	serverSocket.sendto(serialized, address)


def is_room_valid(message_from_client, address):
	"""checks if the room is valid and available in the rooms.txt

	:param message_from_client:
	:param address:
	:return: True or False upcn validation
	"""
	if message_from_client.decode().split(' ')[1] not in get_rooms():
		message_to_client = "Input for Room is not valid or format is not right. " \
							"\nReservation Unsuccessful\nPlease Try again"
		send_message_to_client(message_to_client, address)
		return False
	else:
		return True


def is_timeslots_valid(message_from_client, address):
	"""checks if the time slot is valid and available in timeslots.txt

	:param message_from_client: request made by the client
	:param address: client's address
	:return: True or False upcn validation
	"""
	if message_from_client.decode().split(' ')[2] not in getTime():
		message_to_client = "Input for Time Slot is not valid or format is not right. " \
							"\nReservation Unsuccessful\nPlease Try again "
		send_message_to_client(message_to_client, address)
		return False
	else:
		return True

def is_day_valid(message_from_client, address):
	"""checks if the time slot is valid and available in days.txt

	:param message_from_client:
	:param address: client's address
	:return: True or False upcn validation
	"""
	if message_from_client.decode().split(' ')[3] not in get_days():
		message_to_client = "Input for Days is not valid or format is not right. " \
							"\nReservation Unsuccessful.\nPlease Try again."
		send_message_to_client(message_to_client, address)
		return False
	else:
		return True

### All the messages are handled in this while loop

while True:
	# Receive the client packet along with the address it is coming from
	message_from_client, address = serverSocket.recvfrom(1024)

	if message_from_client.decode() == 'days':
		message_to_client = get_days()
		send_message_to_client(message_to_client, address)

	elif message_from_client.decode() == 'rooms':
		message_to_client = get_rooms()
		send_message_to_client(message_to_client, address)

	elif message_from_client.decode() == 'timeslots':
		message_to_client = getTime()
		send_message_to_client(message_to_client, address)

	elif message_from_client.decode().split(' ')[0] == 'check':
		room_number = message_from_client.decode().split(' ')[1]
		message_to_client = check_reservation(room_number)
		# Checks if the list is actually empty
		if (len(message_to_client) != 0):
			send_message_to_client(message_to_client, address)
		else:
			error_message = "No Reservation found for this room or you may have typed wrong"
			send_message_to_client(error_message, address)

	elif message_from_client.decode().split(' ')[0] == 'delete':
		delete_a_reservation(message_from_client, address)

	elif message_from_client.decode().split(' ')[0] == 'reserve':
		add_reservation(message_from_client, address)

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
