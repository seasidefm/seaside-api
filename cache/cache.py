import os
from redis import Redis


class Cache:
    def __init__(self):
        host = os.environ.get('REDIS_HOST', default="localhost")
        self.cache = Redis(host=host, port=6379)

    def store_in_cache(self, key: str, data, expires=None):
        return self.cache.set(key, data, ex=expires)

    def read_from_cache(self, key: str):
        return self.cache.get(key)

    def clear_key(self, key: str):
        return self.cache.delete(key)
