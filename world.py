import json

from stord import get, put


def get_room(x, y):
    room_raw = get(
        'GRID:%s,%s' % (str(x), str(y))
    )
    return json.loads(room_raw)


def put_room(x, y, room_data):
    put(
        'GRID:%s,%s' % (str(x), str(y)),
        json.dumps(room_data)
    )
    return room_data


def remove_from_room(player):
    room_raw = get(
        'GRID:%s,%s' % (str(player.x), str(player.y))
    )
    room_data = json.loads(room_raw) if room_raw else {
        'players': [player.name]
    }
    if room_data['players'].count(player.name):
        room_data['players'].remove(player.name)
    put('GRID:%s,%s' % (str(player.x), str(player.y)), json.dumps(room_data))


def add_to_room(player):
    put('PLAYER:%s' % player.name, json.dumps(player.__dict__))
    room_raw = get(
        'GRID:%s,%s' % (str(player.x), str(player.y))
    )
    room_data = json.loads(room_raw) if room_raw else {'players': []}

    room_data['players'].append(player.name)
    put('GRID:%s,%s' % (str(player.x), str(player.y)), json.dumps(room_data))
