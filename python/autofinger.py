#!/usr/bin/env python
# -*-coding: utf8 -*-

from time import sleep
import serial
from random import randint
from bs4 import BeautifulSoup
import urllib
import sys
import datetime

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
    'unknown': [90, 160],
}

devs = {
    'OverloadUT': 'seat-1-1',
}

class Arduino:
    ser = None
    state = 'reset'

    def __init__(self):
        try:
            with open('arduino.conf', 'r') as f:
                port = f.readline().rstrip()
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

    def returntocenter(self):
        self.send("allinone090090000000000")

def main():
    global arduino

    last_saved_commit = None

    repos = []
    try:
        with open('repos.conf', 'r') as f:
            for line in f:
                line = line.rstrip()
                repos.append(line.split(','))
    except:
        print "Error reading repos.conf file."
    else:
        while True:
            newest_commit = last_saved_commit
            for repo in repos:
                try:
                    f = urllib.urlopen(repo[2])
                    soup = BeautifulSoup(f.read())
                except IOError:
                    print "ERROR reaching server \"{}\". Will try again later.".format(repo[2])
                else:
                    commit = {}
                    commit_soup_tag = soup.find('item')
                    # Datetime format example: Mon, 21 Apr 2014 23:39:17 +0000
                    # strptime doesn't work with the timezone number, so we strip it out below
                    commit['datetime'] = datetime.datetime.strptime(commit_soup_tag.find_next('pubdate').string[:-6], '%a, %d %b %Y %H:%M:%S')
                    commit['author'] = commit_soup_tag.find_next('author').string
                    commit['project'] = repo[0]
                    commit['color'] = repo[1]
                    if newest_commit == None or commit['datetime'] > newest_commit['datetime']:
                        newest_commit = commit

            if newest_commit != None and (last_saved_commit == None or last_saved_commit['datetime'] < newest_commit['datetime']):
                last_saved_commit = newest_commit
                # We have a new commit!newest_commit
                print "New commit by {}: {}".format(last_saved_commit['author'], last_saved_commit['datetime'])
                send_commands(last_saved_commit, arduino)
                print "Last commit was {} ago".format(datetime.datetime.utcnow() - last_saved_commit['datetime'])

            sleep(5)

def send_commands(commit, arduino):
    seat_coords = [90,90]
    try:
        seat_coords = seats[devs[commit['author']]]
    except KeyError:
        print "Unknown dev: {}".format(commit['author'])

    color = commit['color']
    command = "allinone{0:03d}{1:03d}{2:s}".format(seat_coords[0], seat_coords[1], color).ljust(32)
    arduino.send(command)

if __name__ == '__main__':
    arduino = Arduino()

    try:
        main()
    except KeyboardInterrupt:
        print "Aborted by user."
    finally:
        print "Resetting finger to center position..."
        sleep(2)
        arduino.returntocenter()
        print "Bye!"
        raise
        exit()
