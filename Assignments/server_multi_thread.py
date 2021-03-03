import socket
import struct
import threading, time
import sys

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# UDP config
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

class ClientThread(threading.Thread):
    def __init__(self, data, address, id):
        threading.Thread.__init__(self)
        self.data = data
        self.address = address
        self.id = id
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def run(self):
        print("Start executing client thread: ", self.id)
        capitalizedSentence = data.decode().upper()
        sock.sendto(capitalizedSentence.encode(), address)

        print("End executing client thread: ", self.id)

# Receive/respond loop

thread_count = 0
threads = []
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)
    thread_count += 1
    newthread = ClientThread(data, address, thread_count)
    newthread.start()
    threads.append(newthread)
    time.sleep(3)
    newthread.stop()

    if newthread.is_alive():
        print("Thread still Alive")
    else:
        print("Killed")

for t in threads:
     t.join()