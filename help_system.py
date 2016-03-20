import typing
import os
from ui import ReprTriggeredFunction


def help_function(topic: str = 'help') -> str:

    try:
        with open(os.path.join('help', topic) + ".txt") as tfile:
            return tfile.read()
    except:
        return "Topic not found. To get started just type 'help'."


help_system = ReprTriggeredFunction(help_function)
