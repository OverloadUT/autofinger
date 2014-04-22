from autofinger import seats
from autofinger import Arduino
from random import randint
from time import sleep

colors = [
    "255000000",
    "255255000",
    "000255000",
    "000255255",
    "000000255",
    "255000255",
]

def main():
    global arduino

    seats_sorted = sorted(seats, key=lambda key: key)
    print seats_sorted
    while True:
        for seatkey in seats_sorted:
            print seatkey
            command = "allinone{0:03d}{1:03d}{2}".format(seats[seatkey][0], seats[seatkey][1], colors[randint(0,5)]);

            arduino.send(command)
            sleep(1.2)


if __name__ == '__main__':
    arduino = Arduino()

    try:
        main()
    except KeyboardInterrupt:
        print "Aborted by user."
    finally:
        print "Resetting finger to center position..."
        sleep(2)
        arduino.force_reset()
        print "Bye!"
        raise
        exit()