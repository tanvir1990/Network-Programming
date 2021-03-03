# A simple Room-Booking Application using UDP

A simple CLI-based Room-booking application using Python and UDP socket Programming. Client would type in some commands to interact with the server. Then, these commands are processed in a server and messages are sent back to the client. 

## Requirements
1. Client will type in the following commands to interact with the system.
• 'days': returns the list of all days for which a reservation can be made
• 'rooms': returns a list of all rooms for which reservations can be made
• 'timeslots': returns a list of all timeslots for which a reservation can be made
• 'check <room>': returns all existing reservations for <room>
• 'reserve <room> <timeslot> <day>': enters a reservation for <room> during time <timeslot> for day <day>
• 'delete <room> <timeslot> <day>': delete a reservation for <room> during time <timeslot> for day <day>
• 'quit': server updates file reservations.txt and quits

2. The server should implement checks to ensure that requests are sensible. For example, a reserve request can only be made for a valid room, timeslot, and day, and should not conflict with an already existing reservation. Similarly, deleting a reservation should result in an error message to the user if such a reservation does not exist.
3. The reservations.txt, rooms.txt, days.txt, and timeslots.txt will work as "Database" and store the information of updated reservations, rooms, days, and timeslots respectively
4. The server, upon starting up, has to read in the information from these text files. The information in rooms.txt, days.txt, timeslots.txt will not change during the server’s lifetime. Reservations will come and go as the client interacts with the server. Ultimately, when the application terminates, the file needs to reflect the set of reservations at that point, so if the server is restarted, it can get an up-to-date view of the existing reservations
5. The client cannot wait indefinitely for a reply to a message. The client can wait up to one second for a reply; if no reply is received, then the client should assume that the packet was lost during transmission across the network.
6. 


## How to run
1. **The Server**
To initially run the application, run the server first
command:
in windows: python server.py port
in linux: python3 server.py port
where port is the port number the server listens on. POrt number must be greater than 1024.
2. **The client**
To run the client,
in windows: python client.py host port
in linux: python3 client.py host port

3. Then type in one of the commands mentioned in the Requirements section to interact with the system.


Have Fun!
