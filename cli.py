#!/usr/bin/env python
import argparse
import json

import requests
import tortilla
import click


@click.command()
@click.option('--host', default=None, help='grid server')
@click.option('--token', default=None, help='user token')
@click.argument('command')
def cli(host, token, command):

    with open('grid.json') as gridjson:
        json_dict = json.loads(gridjson.read())
        grid = tortilla.wrap(json_dict['host'])
        grid.config.headers.token = json_dict['token'] # TODO set this up
        auth = {'token': json_dict['token']}

    import ipdb; ipdb.set_trace()
    print(grid.world.get(params=auth))



if __name__ == '__main__':
    cli()
