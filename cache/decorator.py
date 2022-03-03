import json

from cache.cache import Cache

cache = None


def use_cache():
    global cache
    if cache is None:
        cache = Cache()
        return cache

    return cache


def cached(key: str, data_formatter=None, parse_json=False):
    def _cached(func):
        # Get access to cache instance
        c = use_cache()

        # Wrap function
        def wrapper(*args, **kwargs):
            cached_value = c.read_from_cache(key)

            if cached_value is None:
                # call passed function with expected args
                new_value = func(*args, **kwargs)
                # format according to passed args
                formatted = data_formatter(new_value) if data_formatter is not None else new_value
                print(formatted)

                # Store formatted data
                c.store_in_cache(key, formatted)

                return json.loads(formatted) if parse_json else cached_value

            return json.loads(cached_value) if parse_json else cached_value

        return wrapper

    return _cached
