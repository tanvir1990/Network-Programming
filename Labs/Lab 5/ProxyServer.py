
from socket import *
import sys
import traceback

if len(sys.argv) <= 1:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
	sys.exit(2)
	
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start
serverip = sys.argv[1]
tcpSerPort = int(sys.argv[2])

# The following commented values are for testing purpose. PLease ignore
# tcpSerPort = 8888
# serverip = "127.0.0.1"

tcpSerSock.bind((serverip, tcpSerPort))
tcpSerSock.listen(1)
# Fill in end

while 1:
	# Start receiving data from the client
	print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('Received a connection from:', addr)
	# Fill in start
	message = tcpCliSock.recv(1024).decode()
	# Fill in end
	print(message)
	# suppress processing of requests for favicon
	if message.split()[1] == "/favicon.ico":
		print("Suppress request for favicon")
		continue
	filename = message.split()[1].partition("/")[2]
	fileExist = "false"
	filetouse = "/" + filename.replace("/","-")
	print("File to use " + filetouse)
	try:
		# Check wether the file exist in the cache
		f = open(filetouse[1:], "r")                      
		outputdata = f.readlines()                        
		fileExist = "true"
		print("Service file from cache")
		# ProxyServer finds a cache hit and generates a response message
		tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())            
		tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())

		# Fill in start
		for i in range(0, len(outputdata)):
			tcpCliSock.send(outputdata[i].encode())
		# Fill in end

	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false": 
			# Create a socket on the proxyserver
			# Fill in start
			print ('Creating socket on proxyserver')
			c = socket(AF_INET, SOCK_STREAM)
			# Fill in end
			hostn = filename.split("/")[0].replace("www.","",1)         
			print("Host " + hostn)                                   
			try:
				# Connect to the socket to port 80
				# Fill in start
				c.connect((hostn, 80))
				print ('Socket connected to port 80 of the host')
				# Fill in end
				message = "GET "+ "http://" + filename + " HTTP/1.0\r\n\r\n"
				c.send(message.encode())

				# Read the response into buffer
				# Fill in start
				response = c.recv(1024).decode()
				others, html_element = response.split("Content-Type: text/html\r\n")

				# Fill in end

				# Create a new file in the cache for the requested file.
				# Also send the response in the buffer to client socket and the corresponding file in the cache
				tmpFile = open("./" + filetouse, "w")

				# Fill in start
				tmpFile.write(html_element)
				tmpFile.close()
				tcpCliSock.send(response.encode())
				# Fill in end

			except:
				print("Illegal request")
				traceback.print_exc()                                              
		else:
			# HTTP response message for file not found
			# Fill in start
			tcpCliSock.send("HTTP/1.0 404 Not Found\r\n").encode()
			tcpCliSock.send("Content-Type:text/html\r\n").encode()
			# Fill in end
	
	# Close the client and the server sockets
	tcpCliSock.close()

# Fill in start
tcpSerSock.close()
# Fill in end
