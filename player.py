import json

from world import remove_from_room, add_to_room, get_room, put_room
from stord import get, put

def get_player(player):
    return json.loads(
        get('PLAYER:%s' % player)
    )


class Player(object):
    "Core player object, keeping state."
    def __init__(self, name=None):
        if name:
            self.__dict__ = get_player(name)
        else:
            self.name = "an anonymous user"
            self.health = 100
            self.x = 0
            self.y = 0
            self.pow = 0

        if self.name not in get('GRID:%s,%s' % (str(self.x), str(self.y))):
            raise Exception(
                "Player no longer in room. This is an error."
                "If this persists, please contact oatman@bgr0.com."
            )

        add_to_room(self)


    def status(self, *args):
        "Show current GRID position."
        room_data = get_room(self.x, self.y)
        room_data['players'].remove(self.name)

        if room_data['players']:
            return("HERE: " + ", ".join(room_data['players']))
        if room_data.get('data'):
                for n, datum in enumerate(room_data.get('data')):
                    return("DATA #" + str(n) + " " + datum.split('\n')[0])
        return (self.x, self.y)

    def up(self, *args):
        remove_from_room(self)
        self.y = self.y + 1
        add_to_room(self)
        return (self.x, self.y)

    def down(self, *args):
        remove_from_room(self)
        self.y = self.y - 1
        add_to_room(self)
        return (self.x, self.y)

    def right(self, *args):
        remove_from_room(self)
        self.x = self.x + 1
        add_to_room(self)
        return (self.x, self.y)

    def left(self, *args):
        remove_from_room(self)
        self.x = self.x - 1
        add_to_room(self)
        return (self.x, self.y)

    def traverse(self, x, y):
        remove_from_room(self)
        self.x = self.x + x
        self.y = self.y + y
        add_to_room(self)
        return (self.x, self.y)

    def quit(self):
        remove_from_room(self)

    def save(self):
        put('PLAYER:%s' % self.name, json.dumps(self.__dict__))

