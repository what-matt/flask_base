import json
import os

import click
from progress.bar import Bar
from flask import current_app

from app.core import get_redis_timeseries_connection
from app.dao.redis import MenuDaoRedis
from app.schema import FlatMenuSchema
from app.dao.redis.key_schema import KeySchema

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_SITES_FILENAME = os.path.join(ROOT_DIR, "fixtures", "menus.json")


@click.option(
    "-f",
    "--filename",
    default=DEFAULT_SITES_FILENAME,
    help="The filename containing the JSON to load. (default: fixtures/menus.json)")
@click.option(
    "-t",
    "--delete-keys",
    default=False,
    is_flag=True,
    help="Delete any existing redisolar keys before loading")
def load(filename, delete_keys):
    """Load the specified JSON file into Redis"""
    conf = current_app.config
    hostname = conf['REDIS_HOST']
    port = conf['REDIS_PORT']
    key_prefix = conf['REDIS_KEY_PREFIX']
    key_schema = KeySchema(key_prefix)
    client = get_redis_timeseries_connection(hostname=hostname, port=port)
    menu_dao = MenuDaoRedis(client, key_schema)

    if delete_keys:
        for key in client.scan_iter(f"{key_prefix}:*"):
            client.delete(key)

    with open(filename, 'r') as f:
        # menus = [d for d in json.loads(f.read())]
        menus = [FlatMenuSchema().load(d) for d in json.loads(f.read())]

    menus_bar = Bar('Loading menus', max=len(menus))
    p = client.pipeline(transaction=False)
    for menu in menus:
        menus_bar.next()
        menu_dao.insert(menu, pipeline=p)
        # menu_geo_dao.insert(menu, pipeline=p)
    p.execute()

    print("\nFinishing up...")
    p.execute()

    print("\nData load complete!")
