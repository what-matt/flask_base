import datetime

DEFAULT_KEY_PREFIX = "app-test"


def prefixed_key(f):
    """
    A method decorator that prefixes return values.

    Prefixes any string that the decorated method `f` returns with the value of
    the `prefix` attribute on the owner object `self`.
    """
    def prefixed_method(self, *args, **kwargs):
        key = f(self, *args, **kwargs)
        return f"{self.prefix}:{key}"

    return prefixed_method

class KeySchema:
    """
    Methods to generate key names for Redis data structures.

    These key names are used by the DAO classes. This class therefore contains
    a reference to all possible key names used by this application.
    """
    def __init__(self, prefix: str = DEFAULT_KEY_PREFIX):
        self.prefix = prefix

    @prefixed_key
    def menu_hash_key(self, menu_id: int) -> str:
        """
        menu:info:[menu_id]
        Redis type: hash
        """
        return f"menu:info:{menu_id}"

    @prefixed_key
    def menu_ids_key(self) -> str:
        """
        menu:ids
        Redis type: set
        """
        return "menu:ids"