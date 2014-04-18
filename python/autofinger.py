import github
import json
from time import sleep
import serial
from random import randint

seats = {
    'seat-1-1': [30, 5],
    'seat-1-2': [15, 5],
    'seat-1-3': [0, 5],
    'seat-2-1': [35, 15],
    'seat-2-2': [20, 10],
    'seat-2-3': [165, 175],
    'seat-3-1': [40, 25],
    'seat-3-2': [18, 25],
    'seat-4-1': [80, 30],
    'seat-4-2': [0, 90],
    'seat-5-1': [150, 40],
    'seat-6-1': [150, 20],
    'seat-6-2': [10, 168],
    'seat-6-3': [35, 168],
    'seat-6-4': [60, 171],
    'seat-6-5': [65, 177],
    'seat-6-6': [75, 180],
}

colors = [
    "255000000",
    "255255000",
    "000255000",
    "000255255",
    "000000255",
    "255000255",
]

devs = {
    'OverloadUT': 'seat-1-1',
}

def main():
    ser = serial.Serial('/dev/tty.usbserial-A5025Y07', 9600)

    seats_sorted = sorted(seats, key=lambda key: key)

    while True:

        for seatkey in seats_sorted:
            print seatkey
            commands = []
            # Servo command
            commands.append("movsrvos{0:03d}{1:03d}".format(seats[seatkey][0], seats[seatkey][1]))
            # LED command
            #commands.append("stledcol{0:03d}{1:03d}{2:03d}".format(randint(1,2)*128,randint(1,2)*128,randint(1,2)*128))
            commands.append("stledcol{}".format(colors[randint(0,5)]))

            for command in commands:
                print "Command: *{}*".format(command)
                bytecommand = list(bytearray(command))
                ser.write(bytecommand)
                #sleep(1.5)
            sleep(1.2)

    gh = github.GitHub()

    last_saved_commit = None

    while True:
        commits = gh.repos('OverloadUT')('IGC2CSV').commits.get()
        print json.dumps(commits, indent=4, sort_keys=True)
        #TODO: get latest commit
        last_commit = commits[0]

        if last_commit.sha != last_saved_commit:
            last_saved_commit = last_commit.sha
            # We have a new commit!
            print "New commit by {}: {}".format(last_commit.author.login, last_saved_commit)

            send_commands(last_commit, ser)

            # TODO: Send crap to arduino
            #ser.write

        sleep(5)

def send_commands(commit, ser):
    seat_coords = [90,90]
    try:
        seat_coords = seats[devs[commit.author.login]]
    except KeyError:
        print "Unknown dev: {}".format(commit.author.login)

    color = [255,0,0]

    commands = []
    # Servo command
    commands.append("movsrvos{0:03d}{1:03d}".format(seat_coords[0], seat_coords[1]).ljust(32))
    # LED command
    #commands.append("movsrvos{0:03d}{1:03d}".format(seat_coords[0], seat_coords[1]).ljust(32))

    for command in commands:
        print "Command: *{}*".format(command)
        bytecommand = list(bytearray(command))
        ser.write(bytecommand)

if __name__ == '__main__':
    main()