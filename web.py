"""API."""
from flask import Flask, abort
from flask_restful import Resource, Api, reqparse
import requests
import uuid

from auth import api_key

app = Flask(__name__)
api = Api(app)

base_url = 'http://stord.io/key/'


def get(key):
    """
    Get from stord.
    """
    return requests.get(
        base_url + key,
        {'auth': api_key}
    ).json().get(key)


def put(key, value):
    """
    Put to stord.
    """
    return requests.put(
        base_url + key,
        {'auth': api_key, 'value': value}
    ).json()


class Token(Resource):
    token_args = reqparse.RequestParser()
    token_args.add_argument('username', type=str, help='bad username')
    token_args.add_argument('password', type=str, help='bad password')

    def get(self):
        args = self.token_args.parse_args()
        if get("AUTH:%s" % args['username']) == args['password']:
            token = get('TOKEN:%s' % args['username'])
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
        put('AUTH:%s' % args['username'], args['password'])
        return put('TOKEN:%s' % args['username'], uuid.uuid4())

api.add_resource(Token, '/token/')
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
