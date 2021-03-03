# creating an empty list
door = []

# creating 100 doors with closed = 0
for x in range(100):
    door.append(0)

# two loops, the inner loop incrementing by 1
# to increase the gap by 1
for i in range(100):
    for n in range(i, 100, i+1):
        if door[n] == 0:
            door[n] = 1
        elif door[n] == 1:
            door[n] = 0

    if door[i] == 0:
        status = "close"
    elif door[i] == 1:
        status = "open"

    # print ("Door no", i, "Status", door[i])
    print("Door no", i+1, "Status", status)