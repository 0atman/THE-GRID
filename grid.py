#!/usr/bin/python3
import requests
from getpass import getpass
import json

from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from pygments.lexers import HaskellLexer

from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys


from auth import api_key


base_url = 'http://stord.io/key/'


style = style_from_dict({
    Token.Toolbar: '#ffffff bg:#333333',
})
history = InMemoryHistory()
manager = KeyBindingManager.for_prompt()

def isprime(n):
    """Returns True if n is prime"""
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False

        i += w
        w = 6 - w

    return True

def max_previous_spiral(x, y, offset=0): 
    n = max([abs(x), abs(y)]) + offset
    return 4*n**2 - 4*n+1

def get_spiral_number(x, y):
    """
    radius is zero indexed
    """
    radius = max(abs(x), abs(y))
    mps = max_previous_spiral(x, y)
    mp2s = max_previous_spiral(x, y, -1)

    if x == 0 and y==0:
        return 0

    elif x >= 0 and y >= 0:
        """
        (3, 2) = 30
        if both are +ve,
        max previous spiral,
        add the radius 
        add y
        add radius - x
        QED
        """
        return mps + radius + y + (radius - x)

    elif x <= 0 and y >= 0:
        """
        (-2, 3) = 36
        if x is -ve
        max previous spiral,
        add radius x 3
        add abs x
        + rad - y
        QED
        """
        return mps + (radius * 3) + abs(x) + (radius - abs(y))


    elif x <= 0 and y <= 0:
        """
        (-2, -3) = 44
        if x is -ve
        max previous spiral,
        add radius x 5
        add abs y
        + rad - abs x
        """
        return mps + (radius * 5) + abs(y) + (radius - abs(x))

    elif x >= 0 and y <= 0:
        if abs(x) > abs(y):
            """
            (3, -2) = 26
            (4, -2) = 51
            if x > abs y:
            max previous spirals
            + rad - abs x
            + rad - abs y
            """
            return mps + radius - abs(x) + radius - abs(y)
        else:
            """
            (2, -3) = 48
            if x <= abs y
            max previous spirals
            + r * 7
            + abs x
            + rad - abs y
            """
            return mps + (radius * 7) + abs(x) + (radius - abs(y))


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
        print(
            "Write your note below, "
            "to finish put a period '.' on a line by itself"
        )
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
                    raise  # print("Bad note ID.")
                except IndexError:
                    raise  # print("Can't find that note ID")
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
            print(
                "Already logged in."
                "If this is in error, please contact oatman@bgr0.com."
            )
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


@manager.registry.add_binding(Keys.Down)
def _(event):
    event.cli.run_in_terminal(p.south)

@manager.registry.add_binding(Keys.Up)
def _(event):
    event.cli.run_in_terminal(p.north)

@manager.registry.add_binding(Keys.Left)
def _(event):
    event.cli.run_in_terminal(p.west)

@manager.registry.add_binding(Keys.Right)
def _(event):
    event.cli.run_in_terminal(p.east)


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
        print('GRID ONLINE')
        while(True):
            name = input("What is your name chummer? ")
            password = getpass()
            if get("AUTH:%s" % name) == password:
                print("LOGIN OK")
                p.name = name
                p.initialise()
                break
            elif get("AUTH:%s" % name):
                print("PASSWORD INCORRECT")
            else:
                register = input("No one here with that name, register? Y/N: ")
                if register.lower() in ['yes', 'y']:
                    put('AUTH:%s' % name, password)
                    print("%s registered and logged in." % name)
                    p.name = name
                    p.initialise(new=True)
                    break

        print("(type help to get a list of commands)\n")
        print("%s enters THE GRID." % p.name)
        p.status()

        def get_bottom_toolbar_tokens(cli):
            spn = get_spiral_number(p.x, p.y)
            prime = isprime(spn)
            prompt_text = position(p) + ":" + str(spn) + ":" + ("RANDOM ENCOUNTER" if prime else "")
            return [(Token.Toolbar, ' %s ' % prompt_text)]

        while(p.health > 0):
            

            line = prompt(
                '> ',
                get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
                style=style,
                lexer=PygmentsLexer(HaskellLexer),
                completer=WordCompleter(Commands.keys()),
                history=history,
                auto_suggest=AutoSuggestFromHistory(),
                key_bindings_registry=manager.registry
            )
            args = line.split()

            if args and Commands.get(args[0]):
                Commands[args[0]](*args[1:])
            else:
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
