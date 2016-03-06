#!/usr/bin/python3
import requests
from getpass import getpass
import json
from pprint import pprint

from auth import api_key


base_url = 'http://stord.io/key/'


def get(key):
    return requests.get(
        base_url + key,
        {'auth': api_key}
    ).json().get(key)


def put(key, value):
    return requests.put(
        base_url + key,
        {'auth': api_key, 'value': value}
    ).json()


def remove_from_room(player):
    room_raw = get(
        'GRID:%s,%s' % (str(p.x), str(p.y))
    )
    room_data = json.loads(room_raw) if room_raw else {'players': [p.name]}
    if room_data['players'].count(p.name):
        room_data['players'].remove(p.name)
    put('GRID:%s,%s' % (str(p.x), str(p.y)), json.dumps(room_data))


def add_to_room(player):
    put('PLAYER:%s' % p.name, json.dumps(p.__dict__))
    room_raw = get(
        'GRID:%s,%s' % (str(p.x), str(p.y))
    )
    room_data = json.loads(room_raw) if room_raw else {'players': []}

    room_data['players'].append(p.name)
    put('GRID:%s,%s' % (str(p.x), str(p.y)), json.dumps(room_data))


class Player(object):
    "Core player object, keeping state."
    def __init__(self):
        self.name = "An anonymous user"
        self.health = 100
        self.x = 0
        self.y = 0

    def quit(self):
        print("\n%s jacks out of THE GRID. Goodbye." % self.name)
        remove_from_room(self)
        self.health = 0

    def help(self):
        print("Commands:", ", ".join(Commands.keys()))

    def status(self):
        room_raw = get(
            'GRID:%s,%s' % (str(p.x), str(p.y))
        )
        room_data = json.loads(room_raw)
        room_data['players'].remove(p.name)
        print("GRID(%d,%d)" % (p.x, p.y))
        if room_data['players']:
            print("HERE: " + ", ".join(room_data['players']))

    def north(self):
        remove_from_room(p)
        self.y = self.y + 1
        add_to_room(p)
        self.status()

    def south(self):
        remove_from_room(p)
        self.y = self.y - 1
        add_to_room(p)
        self.status()

    def east(self):
        remove_from_room(p)
        self.x = self.x + 1
        add_to_room(p)
        self.status()

    def west(self):
        remove_from_room(p)
        self.x = self.x - 1
        add_to_room(p)
        self.status()

    def initialise(self, new=False):
        if new:
            put('PLAYER:%s' % p.name, json.dumps(p.__dict__))
        p.__dict__ = json.loads(get('PLAYER:%s' % p.name))

        if p.name in get('GRID:%s,%s' % (str(p.x), str(p.y))):
            print("Already logged in. If this is in error, please contact oatman@bgr0.com.")
            raise

        add_to_room(self)


def get_room(x, y):
    room_raw = get(
        'GRID:%s,%s' % (str(x), str(y))
    )
    return json.loads(room_raw) if room_raw else {'players': []}


def scan():
    for y in reversed(range(0, 10)):
        print([
            len(get_room(x, y)['players'])
            for x in range(0, 10)
        ])


if __name__ == '__main__':

    p = Player()

    Commands = {
      'quit': p.quit,
      'help': p.help,
      'status': p.status,
      'north': p.north,
      'south': p.south,
      'east': p.east,
      'west': p.west,
      'scan': scan
      }
    try:
        while(True):
            name = input("What is your name chummer? ")
            password = getpass()
            if get("AUTH:%s" % name) == password:
                print("LOGIN OK")
                p.name = name
                break
            elif get("AUTH:%s" % name):
                print("PASSWORD INCORRECT")
            else:
                register = input("No one here with that name, register? Y/N: ")
                if register.lower() in ['yes', 'y']:
                    put('AUTH:%s' % name, password)
                    print("%s registered and logged in.", name)
                    p.name = name
                    add_to_room(p)
                    break

        p.initialise()

        print("(type help to get a list of commands)\n")
        print("%s enters THE GRID." % p.name)
        p.status()

        while(p.health > 0):
            line = input("> ")
            args = line.split()
            if len(args) > 0:
                commandFound = False
            for c in Commands.keys():
                if args[0] == c[:len(args[0])]:
                    Commands[c]()
                    commandFound = True
                    break
            if not commandFound:
                if args[0] == 'debug' and p.name == 'oatman':
                    import ipdb; ipdb.set_trace()
                print("SYNTAX ERROR (type 'help' for commands)")
    except Exception as e:
        print(e)
        p.quit()
