import json

import requests
from fn.func import curried

from auth import api_key


base_url = 'http://stord.io/key/'


@curried
def get(key):
    return requests.get(
        base_url + key,
        {'auth': api_key}
    ).json().get(key)


@curried
def put(key, value):
    return requests.put(
        base_url + key,
        {'auth': api_key, 'value': value}
    ).json()
