from autofinger import seats
from autofinger import colors
from autofinger import Arduino
from random import randint
from time import sleep

def main():
    arduino = Arduino()

    seats_sorted = sorted(seats, key=lambda key: key)
    while True:
        for seatkey in seats_sorted:
            print seatkey
            commands = []
            commands.append("allinone{0:03d}{1:03d}{2}".format(seats[seatkey][0], seats[seatkey][1], colors[randint(0,5)]));

            for command in commands:
                arduino.send(command)
            sleep(1.2)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted by user. Bye!"
        exit()