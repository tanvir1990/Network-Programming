def check_reservation(room_number):
    file_reservation = open("reservations.txt", 'r')
    dict_reservation = []
    for lines in file_reservation:
        if lines.split()[0] == room_number:
            dict_reservation.append(lines.strip())
    file_reservation.close()
    return dict_reservation
