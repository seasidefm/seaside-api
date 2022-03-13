import bson
import pymongo

from cache.cache_decorator import clear_cache, cached
from database.aggregates import song_score_aggregate, FAVE_SCORE, all_songs_ranked
from database.get_db import get_db
from shared.bson_utils import bson_dumps
from shared.types import Fave


class FaveController:
    collection_name = 'favorites'
    points_per_fave = FAVE_SCORE

    def __init__(self):
        db = get_db("fave-controller")
        self.collection = db.get_collection(self.collection_name)

    def get_count(self, song: str) -> int:
        return self.collection.count_documents({"song": song})

    def get_fave_points(self) -> list:
        return self.collection.aggregate(song_score_aggregate(self.points_per_fave))

    @cached('aggregate_scores', data_formatter=bson_dumps, parse_json=True)
    def get_aggregate_scores(self):
        return self.collection.aggregate(all_songs_ranked)

    @clear_cache(['heat', 'fave_counts', 'aggregate_scores'])
    def add_fave(self, fave: Fave) -> bool:
        existing_fave = self.collection.find_one({"user_id": fave.user, "song": fave.song})

        if existing_fave is not None:
            return False

        else:
            self.collection.insert_one(fave.to_dict())
            return True

    @clear_cache('fave_counts')
    def del_fave(self, fave_id: str):
        return self.collection.delete_one({
            "_id": bson.ObjectId(fave_id)
        })

    def get_faves_for_user(self, user_id: str, sort=pymongo.DESCENDING, limit=None):
        return self.collection.find(
            {"user_id": user_id},
            sort=[('timestamp', sort)]
        ).limit(limit or 0)

