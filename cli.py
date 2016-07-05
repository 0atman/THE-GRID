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
        auth = {'token': json_dict['token']}

    print(grid.world.get(params=auth))

if __name__ == '__main__':
    cli()
