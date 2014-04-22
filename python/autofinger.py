#!/usr/bin/env python
# -*-coding: utf8 -*-

from time import sleep
import serial
from random import randint
from bs4 import BeautifulSoup

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

class Arduino:
    ser = None
    def __init__(self):
        try:
            with open('arduino.conf', 'r') as f:
                port = f.readline()
                print "Arduino port: \"{}\"".format(port)
            self.ser = serial.Serial(port, 9600)
        except IOError:
            print "****  arduino.conf does not exist  ****"
            print "**** Continuing in SIMULATION MODE ****"
        except OSError:
            print "****   ERROR OPENING ARDUINO PORT  ****"
            print "**** Continuing in SIMULATION MODE ****"

    def send(self, command):
        print "Sending command to Arduino: \"{}\"".format(command)
        if self.ser == None:
            print "Simulation mode - Command not sent"
        else:
            bytecommand = list(bytearray(command))
            self.ser.write(bytecommand)

def main():
    arduino = Arduino()

    last_saved_commit = None

    while True:
        #TODO: get latest commit
        last_commit = None

        if last_commit != None and last_commit.sha != last_saved_commit:
            last_saved_commit = last_commit.sha
            # We have a new commit!
            print "New commit by {}: {}".format(last_commit.author.login, last_saved_commit)

            send_commands(last_commit, ser)

            # TODO: Send crap to arduino
            #ser.write

        sleep(5)

def send_commands(commit, arduino):
    seat_coords = [90,90]
    try:
        seat_coords = seats[devs[commit.author.login]]
    except KeyError:
        print "Unknown dev: {}".format(commit.author.login)

    color = [255,0,0]

    commands = []
    # Servo command
    commands.append("movsrvos{0:03d}{1:03d}".format(seat_coords[0], seat_coords[1]).ljust(32))

    for command in commands:
        arduino.send(command)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted by user. Bye!"
        exit()
