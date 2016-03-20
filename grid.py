#!/usr/bin/python3
import requests
from getpass import getpass

from pygments.lexers import HaskellLexer
from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.key_binding.manager import KeyBindingManager

from auth import api_key
from player import Player
import world
from world import get_room
import lis
from help_system import help_system
from ui import get_bottom_toolbar_tokens

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


def scan(*args):
    for y in reversed(range(0, 10)):
        print([
            len(get_room(x, y)['players'])
            for x in range(0, 10)
        ])
'''

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
'''


def grid_prompt(text='> '):
    return prompt(
        text,
        get_bottom_toolbar_tokens=toolbar_tokens,
        style=style,
        lexer=PygmentsLexer(HaskellLexer),
        completer=WordCompleter([]),
        history=history,
        auto_suggest=AutoSuggestFromHistory(),
        key_bindings_registry=manager.registry
    )


if __name__ == '__main__':

    try:
        p = Player()

        # Commands = {
        #   'quit': p.quit,
        #   'help': help,
        #   'look': look,
        #   'status': p.status,
        #   'scan': scan,
        #   'notes': p.notes
        # }
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

        toolbar_tokens = get_bottom_toolbar_tokens(p)
        environ = lis.standard_env(player=p, world=world)
        environ.update({
            'pup': lambda x: bool([p.north() for i in range(x)]),
            'help': help_system,
            'quit': p.quit,
            'help': help,
            # 'look': look,
            'status': p.status,
            'scan': scan,
            'notes': lambda *args: p.notes({}, *args)
        })
        lis.repl(environment=environ, prompt_func=grid_prompt)
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
    except Exception as e:
        if p.name == 'oatman':
            raise e
    finally:
        p.quit()
