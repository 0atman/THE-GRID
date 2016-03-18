from fn.func import curried
from prompt_toolkit.token import Token
import json

from spiral import is_prime_grid
from stord import get


class ReprTriggeredFunction(object):
    """
    Clever use of __repr__ inspired by Brandon Rhodes:
    http://github.com/brandon-rhodes/python-adventure

    Wrap a function in this, and it can be called with no args
    by typing it into the repl.

    >>> c = ReprTriggeredFunction(lambda: "Hello World")
    >>> c
    Hello World
    >>> c()
    'Hello World'
    """
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return self.f(*args, **kwargs)


def position(player):
    room_raw = get(
        'GRID:%s,%s' % (str(player.x), str(player.y))
    )
    room_data = json.loads(room_raw)
    room_data['players'].remove(player.name)
    return "NODE(%0.2X,%0.2X)" % (player.x, player.y)


@curried
def get_bottom_toolbar_tokens(player, cli):
    prime = is_prime_grid(player.x, player.y)
    prompt_text = position(player)
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
