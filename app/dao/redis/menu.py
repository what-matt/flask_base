from typing import Set

from app.models import Menu
from app.dao.base import MenuDaoBase
from app.dao.base import MenuNotFound
from app.dao.redis.base import RedisDaoBase
from app.schema import FlatMenuSchema


class MenuDaoRedis(MenuDaoBase, RedisDaoBase):
    """MenuDaoRedis persists Menu models to Redis.

    This class allows persisting (and querying for) Menus in Redis.
    """
    def insert(self, menu: Menu, **kwargs):
        """Insert a Menu into Redis."""
        hash_key = self.key_schema.menu_hash_key(menu.id)
        menu_ids_key = self.key_schema.menu_ids_key()
        client = kwargs.get('pipeline', self.redis)
        client.hset(hash_key, mapping=FlatMenuSchema().dump(menu))
        client.sadd(menu_ids_key, menu.id)

    def insert_many(self, *menus: Menu, **kwargs) -> None:
        for menu in menus:
            self.insert(menu, **kwargs)

    def find_by_id(self, menu_id: int, **kwargs) -> Menu:
        """Find a Menu by ID in Redis."""
        hash_key = self.key_schema.menu_hash_key(menu_id)
        menu_hash = self.redis.hgetall(hash_key)

        if not menu_hash:
            raise MenuNotFound()

        return FlatMenuSchema().load(menu_hash)

    def find_all(self, **kwargs) -> Set[Menu]:
        """Find all Menus in Redis."""
        # START Challenge #1
        menu_hashes = []
        menu_ids_key = self.key_schema.menu_ids_key()
        menu_ids = self.redis.smembers(menu_ids_key)  # type: ignore

        for menu_id in menu_ids:
          hash_key = self.key_schema.menu_hash_key(menu_id)
          menu_hashes.append(self.redis.hgetall(hash_key))
        # END Challenge #1

        return {FlatMenuSchema().load(menu_hash) for menu_hash in menu_hashes}
