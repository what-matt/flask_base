import abc
import datetime
from typing import Iterable
from typing import Set

from app.models import Menu


class MenuNotFound(Exception):
    """A Menu with the given ID does not exist."""

class MenuDaoBase(abc.ABC):
    @abc.abstractmethod
    def insert(self, menu: Menu, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def find_by_id(self, menu_id: int, **kwargs):
        pass

    @abc.abstractmethod
    def find_all(self, **kwargs) -> Set[Menu]:
        pass
