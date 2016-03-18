import typing
from ui import ReprTriggeredFunction


def help_function(topic: str = '') -> str:
    #import ipdb; ipdb.set_trace()

    tutorial = '''
        Welcome chummer.
        It's so nice of you to drop by.
    '''
    if topic and locals().get(topic):
        return locals()[topic]
    else:
        return "This is the lovely help system."


help_system = ReprTriggeredFunction(help_function)
