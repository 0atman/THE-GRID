#!/usr/bin/python3
import requests
from getpass import getpass
import json

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
        self.note_store = []

    def quit(self, *args):
        print("\n%s jacks out of THE GRID. Goodbye." % self.name)
        remove_from_room(self)
        self.health = 0

    def status(self, *args):
        "Show current GRID position."
        room_raw = get(
            'GRID:%s,%s' % (str(p.x), str(p.y))
        )
        room_data = json.loads(room_raw)
        room_data['players'].remove(p.name)
        if room_data['players']:
            print("HERE: " + ", ".join(room_data['players']))
        if room_data.get('data'):
                for n, datum in enumerate(room_data.get('data')):
                    print("DATA #" + str(n) + " " + datum.split('\n')[0])

    def north(self, *args):
        remove_from_room(p)
        self.y = self.y + 1
        add_to_room(p)
        self.status()

    def south(self, *args):
        remove_from_room(p)
        self.y = self.y - 1
        add_to_room(p)
        self.status()

    def east(self, *args):
        remove_from_room(p)
        self.x = self.x + 1
        add_to_room(p)
        self.status()

    def west(self, *args):
        remove_from_room(p)
        self.x = self.x - 1
        add_to_room(p)
        self.status()

    def writenote(self):
        print("Write your note below, to finish put a period '.' on a line by itself")
        input_list = []

        while True:
            input_str = input('" ')
            if input_str == ".":
                break
            else:
                input_list.append(input_str)
        self.note_store.append("\n".join(input_list))
        self.save()

    def notes(self, *args):
        if args:
            if args[0].lower() in ['new', 'create', 'write', 'add']:
                self.writenote()
                return
            if args[0].lower() in ['delete', 'del', 'rm']:
                try:
                    del self.note_store[int(args[1])]
                    self.save()
                except ValueError:
                    print("Bad note ID.")
                except IndexError:
                    print("Can't find that note ID")
                return
            if args[0].lower() in ['drop']:
                try:
                    dropped_note = self.note_store[int(args[1])]
                    del self.note_store[int(args[1])]
                    self.save()
                    room_raw = get(
                        'GRID:%s,%s' % (str(p.x), str(p.y))
                    )
                    room_data = json.loads(room_raw)
                    if not room_data.get('data'):
                        room_data['data'] = []
                    room_data['data'].append(dropped_note)
                    put(
                        'GRID:%s,%s' % (str(p.x), str(p.y)),
                        json.dumps(room_data)
                    )
                except ValueError:
                    raise #print("Bad note ID.")
                except IndexError:
                    raise # print("Can't find that note ID")
                return
            if len(args) == 1:
                try:
                    print(
                        "note #" +
                        str(args[0]) + " " +
                        self.note_store[int(args[0])]
                    )
                    return
                except ValueError:
                    print("Bad note ID.")
                    return
                except IndexError:
                    print("Can't find that note ID")
                    return
        if not self.__dict__.get('note_store'):
            self.note_store = []
            self.save()
        for n, note in enumerate(self.note_store):
            print("note #" + str(n) + " " + note.split('\n')[0])

    def save(self):
        put('PLAYER:%s' % self.name, json.dumps(self.__dict__))

    def initialise(self, new=False):
        if new:
            self.save()
        self.__dict__ = json.loads(get('PLAYER:%s' % p.name))

        if self.name in get('GRID:%s,%s' % (str(p.x), str(p.y))):
            print("Already logged in. If this is in error, please contact oatman@bgr0.com.")
            raise

        add_to_room(self)


def help(*args):
    if args:
        print(Commands.get(args[0]).__doc__)
    else:
        print("Commands:", ", ".join(Commands.keys()))


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


def position(player):
    room_raw = get(
        'GRID:%s,%s' % (str(p.x), str(p.y))
    )
    room_data = json.loads(room_raw)
    room_data['players'].remove(p.name)
    return "GRID(%d,%d)" % (p.x, p.y)

if __name__ == '__main__':

    p = Player()

    Commands = {
      'quit': p.quit,
      'help': help,
      'status': p.status,
      'north': p.north,
      'south': p.south,
      'east': p.east,
      'west': p.west,
      'scan': scan,
      'notes': p.notes,
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
            line = input(position(p) + "> ")
            args = line.split()

            if Commands.get(args[0]):
                Commands[args[0]](*args[1:])
            else:
                if args[0] == 'debug' and p.name == 'oatman':
                    import ipdb; ipdb.set_trace()
                print("SYNTAX ERROR (type 'help' for commands)")
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
    except Exception as e:
        import socket
        if not socket.gethostname() == 'bgr0.com':
            raise e
    finally:
        p.quit()
