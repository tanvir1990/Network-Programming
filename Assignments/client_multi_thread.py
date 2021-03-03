import socket
import struct
import sys

#message = 'very important data'
multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(1)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.ch
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:

    # Send data to the multicast group


    # Look for responses from all recipients
    while True:
        message = input("Enter")    #this is where all client commands will go
        sent = sock.sendto(message.encode(), multicast_group)
        while True:

            print('sending "%s"' % message)

            print('waiting to receive')
            try:
                data, server = sock.recvfrom(16)
            except socket.timeout:
                print('timed out, no more responses')
                break
            else:
                print('received "%s" from %s' % (data.decode(), server))
                break

finally:
    print('closing socket')
    sock.close()