from typing import Set

from app.models import Menu
from app.models import MenuModel
from app.dao.base import MenuDaoBase
from app.dao.base import MenuNotFound
from app.dao.sqlite.base import RedisDaoBase
from app.schema import FlatMenuSchema


class MenuDaoRedis(MenuDaoBase, RedisDaoBase):
    """MenuDaoRedis persists Menu models to Redis.

    This class allows persisting (and querying for) Menus in Redis.
    """
    def insert(self, menu: Menu, **kwargs):
        """Insert a Menu into Redis."""
        menuModel = MenuModel(id=menu.id, name=menu.name, type=menu.type)
        self.db.session.add(menuModel)
        self.db.session.flush()
        self.db.session.commit()

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
        return MenuModel.query.all()
