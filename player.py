import json

from world import remove_from_room, add_to_room, get_room, put_room
from stord import get, put


def get_player(player):
    return json.loads(
        get('PLAYER:%s' % player)
    )


class Player(object):
    "Core player object, keeping state."
    def __init__(self):
        self.name = "An anonymous user"
        self.health = 100
        self.x = 0
        self.y = 0
        self.note_store = []
        self.pow = 0

    def quit(self, *args):
        print("\n%s jacks out of THE GRID. Goodbye." % self.name)
        remove_from_room(self)
        self.health = 0

    def status(self, *args):
        "Show current GRID position."
        room_data = get_room(self.x, self.y)
        room_data['players'].remove(self.name)

        if room_data['players']:
            print("HERE: " + ", ".join(room_data['players']))
        if room_data.get('data'):
                for n, datum in enumerate(room_data.get('data')):
                    print("DATA #" + str(n) + " " + datum.split('\n')[0])

    def north(self, *args):
        remove_from_room(self)
        self.y = self.y + 1
        add_to_room(self)
        self.status()

    def south(self, *args):
        remove_from_room(self)
        self.y = self.y - 1
        add_to_room(self)
        self.status()

    def east(self, *args):
        remove_from_room(self)
        self.x = self.x + 1
        add_to_room(self)
        self.status()

    def west(self, *args):
        remove_from_room(self)
        self.x = self.x - 1
        add_to_room(self)
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
                    room_data = get_room(self.x, self.y)
                    if not room_data.get('data'):
                        room_data['data'] = []
                    room_data['data'].append(dropped_note)

                    put_room(self.x, self.y, room_data)
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
        self.__dict__ = get_player(self.name)

        if self.name in get('GRID:%s,%s' % (str(self.x), str(self.y))):
            print(
                "Already logged in. Try again."
                "If this is in error, please contact oatman@bgr0.com."
            )
            raise

        add_to_room(self)
