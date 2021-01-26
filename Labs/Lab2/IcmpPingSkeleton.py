from socket import *
import os
import sys
import struct
import time
import select
import binascii  
import array

ICMP_ECHO_REQUEST = 8

def chksum(packet):
	if len(packet) % 2 != 0:
		packet += b'\0'
	res = sum(array.array("H", packet))
	res = (res >> 16) + (res & 0xffff)
	res += res >> 16
	return (~res) & 0xffff


def receiveOnePing(mySocket, ID, timeout, destAddr):
	timeLeft = timeout
	
	while 1: 
		startedSelect = time.time()
		whatReady = select.select([mySocket], [], [], timeLeft)
		howLongInSelect = (time.time() - startedSelect)
		if whatReady[0] == []: # Timeout
			return "Request timed out."
	
		timeReceived = time.time() 
		recPacket, addr = mySocket.recvfrom(1024)

		#Fill in start
		#Fetch the ICMP header from the IP packet, extract relevant fields and generate output
		ipHeader = recPacket[:20]
		ipVer, servType, length, ipID, ipFlagsOff, ipTTL, ipProc, ipChecksum, ipSrc, ipDest = struct.unpack("BBHHHBBHII", ipHeader)

		icmpHeader = recPacket[20:28]
		icmpType, code, checksum, packID, sequence = struct.unpack("bbHHh", icmpHeader)
		if packID == ID:
			timeSent = struct.unpack("d", recPacket[28:28 + struct.calcsize("d")])[0]

			# Print out reply information
			delayMS = (timeReceived - timeSent) * 1000
			packetSize = len(recPacket)

			print ("Reply from " + str(addr[0]) + ": bytes=" + str(packetSize) + " time=" + str(delayMS) + "ms TTL=" + str(ipTTL))

			return delayMS

		#Fill in end 
		
		timeLeft = timeLeft - howLongInSelect
		if timeLeft <= 0:
			return "Request timed out."

	
def sendOnePing(mySocket, destAddr, ID):
	# Header is type (8), code (8), checksum (16), id (16), sequence (16)
	
	myChecksum = 0
	# Make a dummy header with a 0 checksum
	# struct -- Interpret strings as packed binary data
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	data = struct.pack("d", time.time())
	# Calculate the checksum on the data and the dummy header.

	myChecksum = chksum(header + data) 
	
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	packet = header + data
	
	mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
	# Both LISTS and TUPLES consist of a number of objects
	# which can be referenced by their position number within the object.
	
def doOnePing(destAddr, timeout): 
	icmp = getprotobyname("icmp")

	# SOCK_RAW is a powerful socket type. For more details:   http://sock-raw.org/papers/sock_raw
	mySocket = socket(AF_INET, SOCK_RAW, icmp)
	
	myID = os.getpid() & 0xFFFF  # Return the current process i
	sendOnePing(mySocket, destAddr, myID)
	delay = receiveOnePing(mySocket, myID, timeout, destAddr)
	
	mySocket.close()
	return delay
	
def ping(host, timeout=1):
	# timeout=1 means: If one second goes by without a reply from the server,
	# the client assumes that either the client's ping or the server's pong is lost
	dest = gethostbyname(host)
	print("Pinging " + dest + " using Python:")
	print("")
	# Send ping requests to a server separated by approximately one second
	for x in range(10):
		delay = doOnePing(dest, timeout)
		#print(delay)
		time.sleep(1)# one second
	return delay
	
ping("127.0.0.1")



