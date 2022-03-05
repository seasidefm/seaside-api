import json
from functools import wraps

from cache.cache import Cache

cache = None


def use_cache():
    global cache
    if cache is None:
        cache = Cache()
        return cache

    return cache


def clear_cache(key: str):
    """
    Clear the cache at given key on a successful return from wrapped function

    :param key: The cache key to clear
    :return:
    """
    def _clear_cache(func):
        c = use_cache()

        # Wrap function
        @wraps(func)
        def wrapper(*args, **kwargs):
            return_val = func(*args, **kwargs)

            # Clear cached value if execution makes it this far
            c.clear_key(key)

            return return_val

        return wrapper

    return _clear_cache


def cached(key: str, data_formatter=None, parse_json=False):
    """
    This
    :param key: the cache value to set
    :param data_formatter: function for turning returned data to string
    :param parse_json: treat returned cache as JSON deserializable or not
    :return: ?
    """
    def _cached(func):
        # Get access to cache instance
        c = use_cache()

        # Wrap function
        @wraps(func)
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
