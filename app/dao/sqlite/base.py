# from redis.client import Redis

from app.dao.redis.key_schema import KeySchema


class RedisDaoBase:
    """Shared functionality for Redis DAO classes."""
    def __init__(self,
                 db,
                 key_schema: KeySchema = None, **kwargs) -> None:
        self.db = db
        if key_schema is None:
            key_schema = KeySchema()
        self.key_schema = key_schema
