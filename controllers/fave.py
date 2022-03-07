from database.get_db import get_db
from shared.types import Fave


class FaveController:
    collection_name = 'favorites'

    def __init__(self):
        db = get_db("fave-controller")
        self.collection = db.get_collection(self.collection_name)

    def add_fave(self, fave: Fave) -> bool:
        existing_fave = self.collection.find_one({"twitch_id": fave.user, "song": fave.song})

        if existing_fave is not None:
            return False

        else:
            self.collection.insert_one(fave.to_dict())
            return True


