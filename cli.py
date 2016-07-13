#!/usr/bin/env python
import argparse
import json

import requests
import tortilla
import click

from pygments.lexers import HaskellLexer
from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.key_binding.manager import KeyBindingManager
from ui import get_bottom_toolbar_tokens

from command import command_parser

style = style_from_dict({
    Token.Toolbar: '#ffffff bg:#333333',
    Token.Red: '#ff0066',
    Token.Green: '#44ff44',
    Token.Orange: '#ff9900',
    Token.White: '#ffffff',
})

history = InMemoryHistory()
manager = KeyBindingManager.for_prompt()

toolbar_tokens =  lambda _: [
    (Token.Toolbar, ' '),
    (Token.Green, ' GRID ONLINE ')
]
#get_bottom_toolbar_tokens(p)

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


@click.command()
@click.option('--host', default=None, help='grid server')
@click.option('--token', default=None, help='user token')
@click.option('--debug/--no-dubug', default=False)
@click.argument('command')
def cli(host, token, debug, command):

    with open('grid.json') as gridjson:
        json_dict = json.loads(gridjson.read())
        grid = tortilla.wrap(json_dict['host'])
        grid.config.headers.token = json_dict['token']


    while True:
        try:
            val = grid_prompt()
            if val:
                if val == 'exit' or val == 'quit':
                    break
                print(command_parser(grid, *val.split()))
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except Exception as e:
            if debug:
                raise e
            else:
                print('ERROR:', e)
    print('Bye!')

if __name__ == '__main__':
    cli()
