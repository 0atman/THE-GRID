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
from spiral import is_prime_grid, get_spiral_number
from player import Player


base_url = 'http://stord.io/key/'


style = style_from_dict({
    Token.Toolbar: '#ffffff bg:#333333',
})
history = InMemoryHistory()
manager = KeyBindingManager.for_prompt()


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
def down(event):
    event.cli.run_in_terminal(p.south)


@manager.registry.add_binding(Keys.Up)
def up(event):
    event.cli.run_in_terminal(p.north)


@manager.registry.add_binding(Keys.Left)
def left(event):
    event.cli.run_in_terminal(p.west)


@manager.registry.add_binding(Keys.Right)
def right(event):
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
            pow_value = get_spiral_number(p.x, p.y)
            prime = is_prime_grid(p.x, p.y)
            prompt_text = position(p) + (
                ": PROXIMITY WARNING" if prime else ""
            )
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
