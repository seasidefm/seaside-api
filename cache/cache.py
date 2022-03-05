from redis import Redis


class Cache:
    def __init__(self):
        self.cache = Redis(host="localhost", port=6379)

    def store_in_cache(self, key: str, data, expires=None):
        return self.cache.set(key, data, ex=expires)

    def read_from_cache(self, key: str):
        return self.cache.get(key)

    def clear_key(self, key: str):
        return self.cache.delete(key)
