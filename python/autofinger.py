#!/usr/bin/env python
# -*-coding: utf8 -*-

from time import sleep
import serial
from bs4 import BeautifulSoup
import urllib2
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
}

class Devs:
    devseats = {}

    def __init__(self):
        try:
            with open('devs.conf', 'r') as f:
                for line in f:
                    dev = line.rstrip().split(',')
                    self.devseats[dev[0]] = dev[1]
                    print "Loaded dev {} in seat {}".format(dev[0], dev[1])
        except:
            print "Error reading devs.conf"

    def get_seat_name(self, dev):
        if dev in self.devseats and self.devseats[dev] in seats:
            return self.devseats[dev]
        elif dev in self.devseats and self.devseats[dev] == 'ignore':
            return 'ignore'
        else:
            return False

    def get_seat(self, dev):
        if dev in self.devseats and self.devseats[dev] in seats and seats[self.devseats[dev]] != 'ignore':
            return seats[self.devseats[dev]]
        else:
            return False

    def is_defined(self, dev):
        return (dev in self.devseats)

    def has_seat(self, dev):
        if self.is_defined(dev) and self.get_seat_name(dev) != 'ignore':
            return True
        else:
            return False

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

    def force_reset(self):
        self.send("allinone090090000000000")
        self.state = 'reset'

    def reset(self):
        if self.state != 'reset':
            self.force_reset()

    def point(self, seat, color):
        if seat != False:
            command = "allinone{0:03d}{1:03d}{2:s}".format(seat[0], seat[1], color).ljust(32)
            self.send(command)
            self.state = 'pointing'

def main():
    global arduino
    devs = Devs()

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
                    f = urllib2.urlopen(repo[2],None,5)
                    soup = BeautifulSoup(f.read())
                except IOError:
                    print "ERROR reaching server \"{}\". Will try again later.".format(repo[2])
                except:
                    raise
                else:
                    commit_soup_tags = soup.find_all('item')
                    # Datetime format example: Mon, 21 Apr 2014 23:39:17 +0000
                    # strptime doesn't work with the timezone number, so we strip it out below
                    for idx, commit_soup_tag in enumerate(commit_soup_tags):
                        if idx > 3:
                            break;
                        commit = {}
                        commit['datetime'] = datetime.datetime.strptime(commit_soup_tag.find_next('pubdate').string[:-6], '%a, %d %b %Y %H:%M:%S')
                        commit['author'] = commit_soup_tag.find_next('author').string.split('<')[0].rstrip()
                        commit['project'] = repo[0]
                        commit['color'] = repo[1]
                        if devs.has_seat(commit['author']) and (newest_commit == None or commit['datetime'] > newest_commit['datetime']):
                            newest_commit = commit
                sleep(1)

            if newest_commit != None and (last_saved_commit == None or last_saved_commit['datetime'] < newest_commit['datetime']):
                last_saved_commit = newest_commit
                # We have a new commit!newest_commit
                print "New commit by {}: {}".format(last_saved_commit['author'], last_saved_commit['datetime'])
                print "Commit was {} ago".format(datetime.datetime.utcnow() - last_saved_commit['datetime'])
                # Only point if the commit was in the last hour
                if (datetime.datetime.utcnow() - last_saved_commit['datetime']).seconds < 3600:
                    arduino.point(devs.get_seat(last_saved_commit['author']), last_saved_commit['color'])
                else:
                    print "Commit was too old to point"

            sleep(5)

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
