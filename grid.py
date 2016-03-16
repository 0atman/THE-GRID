#!/usr/bin/python3
import requests
from getpass import getpass
import json

from pygments.lexers import HaskellLexer
from fn.func import curried
from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys


from auth import api_key
from spiral import is_prime_grid, get_spiral_number
from player import Player
from world import look, get_room
import lis


base_url = 'http://stord.io/key/'


style = style_from_dict({
    Token.Toolbar: '#ffffff bg:#333333',
    Token.Red: '#ff0066',
    Token.Green: '#44ff44',
    Token.Orange: '#ff9900',
    Token.White: '#ffffff',
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


def help(room, player, *args):
    if args:
        print(Commands.get(args[0]).__doc__)
    else:
        print("Commands:", ", ".join(Commands.keys()))


def scan(*args):
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
    return "NODE(%0.2X,%0.2X)" % (p.x, p.y)


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


def grid_prompt(text='> '):
    return prompt(
        text,
        get_bottom_toolbar_tokens=toolbar_tokens,
        style=style,
        lexer=PygmentsLexer(HaskellLexer),
        completer=WordCompleter(Commands.keys()),
        history=history,
        auto_suggest=AutoSuggestFromHistory(),
        key_bindings_registry=manager.registry
    )


if __name__ == '__main__':

    p = Player()
    environ = lis.standard_env()
    environ.update({
        'pup': lambda x: bool([p.north() for i in range(x)]),
    })

    Commands = {
      'quit': p.quit,
      'help': help,
      'look': look,
      'status': p.status,
      'scan': scan,
      'notes': p.notes,
      'repl': lambda *args: lis.repl(environment=environ, prompt_func=grid_prompt)
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

        @curried
        def get_bottom_toolbar_tokens(player, cli):
            pow_value = get_spiral_number(player.x, player.y)
            prime = is_prime_grid(p.x, p.y)
            prompt_text = position(p)
            tokens = [
                (Token.Toolbar, ' '),
                (Token.Green, ' GRID ONLINE '),
                (Token.Toolbar, ' '),
                (Token.White, ' %s ' % prompt_text),
                (Token.Toolbar, ' '),
                (Token.Orange, ' %d POW ' % player.pow),
            ]
            if prime:
                tokens.append((Token.Toolbar, ' '))
                tokens.append((Token.Red, " PROXIMITY WARNING "))
            return tokens

        toolbar_tokens = get_bottom_toolbar_tokens(p)

        while(p.health > 0):

            line = grid_prompt()
            args = line.split()

            if args and Commands.get(args[0]):

                Commands[args[0]](
                    get_room(p.x, p.y),
                    p,
                    *args[1:]
                )
            else:
                print("SYNTAX ERROR (type 'help' for commands)")
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
    except Exception as e:
        if p.name == 'oatman':
            raise e
    finally:
        p.quit()
