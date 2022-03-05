import time
from functools import wraps

from flask import request

from cache.decorator import use_cache
from database.get_db import get_db

token_error = {
    "not_allowed": ("Token missing or invalid", 403)
}


def token_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        cache = use_cache()
        controller = TokenController()
        token = request.headers.get('Authorization')

        # First handle empty token
        if token == "" or token is None:
            return token_error['not_allowed']

        token_cache_key = f"tcache-{token}"
        # Then handle potential cached token validation
        cached = cache.read_from_cache(token_cache_key)
        if cached is None:
            # Finally, check if token is valid using DB call
            token_object = controller.validate_token(token)
            if token_object is None:
                return token_error['not_allowed']

            expires = int(time.time()) + 600  # 5 minutes
            cache.store_in_cache(token_cache_key, "ADD PERMISSIONS HERE?", expires=expires)

        return func(*args, **kwargs)

    return wrapper


class TokenController:
    collection_name = 'tokens'

    def __init__(self):
        db = get_db()
        self.collection = db.get_collection(self.collection_name)

    def validate_token(self, token: str):
        data = self.collection.find_one({"token": token})

        if data is None:
            return data
        else:
            return dict(data)
