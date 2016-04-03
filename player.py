import json

from world import remove_from_room, add_to_room, get_room, put_room
from stord import get, put
import lis


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

    def up(self, *args):
        remove_from_room(self)
        self.y = self.y + 1
        add_to_room(self)
        self.status()

    def down(self, *args):
        remove_from_room(self)
        self.y = self.y - 1
        add_to_room(self)
        self.status()

    def right(self, *args):
        remove_from_room(self)
        self.x = self.x + 1
        add_to_room(self)
        self.status()

    def left(self, *args):
        remove_from_room(self)
        self.x = self.x - 1
        add_to_room(self)
        self.status()

    def traverse(self, x, y):
        remove_from_room(self)
        self.x = self.x + x
        self.y = self.y + y
        add_to_room(self) 
        return (self.x, self.y)

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

    def notes(self, world, *args):
        if not self.__dict__.get('note_store'):
            self.note_store = []
            self.save()
        if len(args) == 0:
            if self.note_store:
                for n, note in enumerate(self.note_store):
                    print("note #" + str(n) + "\n" + note.split('\n')[0])
            else:
                print("No notes.")

        elif len(args) > 0:
            if str(args[0]).lower() in ['new', 'create', 'write', 'add']:
                self.writenote()
                return
            if str(args[0]).lower() in ['delete', 'del', 'rm']:
                try:
                    del self.note_store[int(args[1])]
                    self.save()
                    print('Deleted.')
                except ValueError:
                    print("Bad note ID.")
                except IndexError:
                    print("Can't find that note ID")
                return
            if str(args[0]).lower() in ['run']:
                try:
                    for line in self.note_store[int(args[1])].split('\n'):
                        val = lis.eval(lis.parse(line))
                        if val:
                            print(lis.lispstr(val))
                    print()
                except IndexError:
                    print("Can't find that note ID")
                return
            if str(args[0]).lower() in ['drop']:
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
            elif type(args[0]) == int:
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
