"""API."""
from functools import wraps
import uuid
from hashlib import sha1
import json

from flask import Flask, abort
from flask import g, request, redirect, url_for
from flask_restful import Resource, Api, reqparse
import requests
import webcolors

from auth import api_key
from spiral import get_spiral_number
from player import Player
from stord import get, put

app = Flask(__name__)
api = Api(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token', None)
        if token and player_name:
            player_name = get('TOKEN_LOOKUP:%s' % token)
            player = Player(player_name)
            return f(args[0], player, *args[1:], **kwargs)
        else:
            abort(403)
    return decorated_function


class Token(Resource):
    token_args = reqparse.RequestParser()
    token_args.add_argument('username', type=str, help='bad username')
    token_args.add_argument('password', type=str, help='bad password')

    def get(self):
        args = self.token_args.parse_args()
        if get("AUTH:%s" % args['username']) == args['password']:
            token = get('TOKEN_USERNAME:%s' % args['username'])
        else:
            abort(403)
        return {
            "token": token
        }

    def put(self):
        args = self.token_args.parse_args()
        passwd = get("AUTH:%s" % args['username'])
        if passwd == args['password']:
            abort(409)
        elif passwd:
            abort(403)
        token = uuid.uuid4()
        put('AUTH:%s' % args['username'], args['password'])
        put('TOKEN_LOOKUP:%s' % token, args['username'])
        return put('TOKEN_USERNAME:%s' % args['username'], token)


class World(Resource):

    def closest_colour(self, requested_colour):
        min_colours = {}
        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]

    def get_colour_name(self, requested_colour):
        try:
            closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
        except ValueError:
            closest_name = self.closest_colour(requested_colour)
            actual_name = None
        return actual_name, closest_name

    @login_required
    def get(self, player):
        x = 3
        y = 3
        number = get_spiral_number(int(x), int(y))
        digest = sha1(str(number).encode('utf-8')).hexdigest()
        colour_tuple = (
            int(digest[-2:], 16),
            int(digest[-4:-2], 16),
            int(digest[-6:-4], 16)
        )
        actual_name, closest_name = self.get_colour_name(colour_tuple)
        colour_name = actual_name if actual_name else closest_name
        gid = 'GRID:%s,%s' % (str(x), str(y))
        room_raw = get(gid)
        room = json.loads(room_raw) if room_raw else {'players': []}
        put(gid, json.dumps(room))
        player.quit()
        return {
            "color": colour_name,
            "player": player.__dict__,
            "room": room
        }

class WorldPosition(Resource):
    position_parser= reqparse.RequestParser()
    position_parser.add_argument('move', dest='movement direction', type=str)

    @login_required
    def put(self, player):
        args = parser.parse_args()
        direction = args['direction']
        return direction

api.add_resource(Token, '/token/')
api.add_resource(World, '/world/')
api.add_resource(WorldPosition, '/world/position/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
