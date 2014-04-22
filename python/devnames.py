from autofinger import seats
from autofinger import Arduino
from autofinger import Devs
from bs4 import BeautifulSoup
import urllib

def main():
    repos = []
    repodevs = {}
    devs = Devs()
    try:
        with open('repos.conf', 'r') as f:
            for line in f:
                line = line.rstrip()
                repos.append(line.split(','))
                print repos[-1]
    except:
        print "Error reading repos.conf file."
    else:
        for repo in repos:
            try:
                f = urllib.urlopen(repo[2])
                soup = BeautifulSoup(f.read())
            except IOError:
                print "ERROR reaching server \"{}\".".format(repo[2])
            else:
                for author in soup.find_all('author'):
                    name = author.string.encode('ascii','replace').split('<')[0].rstrip()
                    repodevs[name] = True

    for repodev in repodevs:
        if devs.is_defined(repodev):
            print "Dev match: {} in seat {}".format(repodev, devs.get_seat_name(repodev))
        else:
            print "NEW DEV FOUND: {}".format(repodev)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Aborted by user."
        exit()