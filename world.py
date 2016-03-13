import json
from hashlib import sha1

import webcolors

from stord import get, put
from spiral import get_spiral_number


def get_room(x, y):
    room_raw = get(
        'GRID:%s,%s' % (str(x), str(y))
    )
    return json.loads(room_raw) if room_raw else {'players': []}


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


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


def look(room, player, x, y):
    number = get_spiral_number(int(x), int(y))
    digest = sha1(str(number).encode('utf-8')).hexdigest()
    colour_tuple = (
        int(digest[-2:], 16),
        int(digest[-4:-2], 16),
        int(digest[-6:-4], 16)
    )
    actual_name, closest_name = get_colour_name(colour_tuple)
    print(actual_name if actual_name else closest_name)