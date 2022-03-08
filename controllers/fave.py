import pymongo

from cache.decorator import clear_cache
from database.get_db import get_db
from shared.types import Fave


class FaveController:
    collection_name = 'favorites'

    def __init__(self):
        db = get_db("fave-controller")
        self.collection = db.get_collection(self.collection_name)

    def get_count(self, song: str) -> int:
        return self.collection.count_documents({"song": song})

    @clear_cache('heat')
    def add_fave(self, fave: Fave) -> bool:
        existing_fave = self.collection.find_one({"user_id": fave.user, "song": fave.song})

        if existing_fave is not None:
            return False

        else:
            self.collection.insert_one(fave.to_dict())
            return True

    def get_faves_for_user(self, user_id: str, sort=pymongo.DESCENDING, limit=None):
        return self.collection.find(
            {"user_id": user_id},
            sort=[('timestamp', sort)]
        ).limit(limit or 0)

