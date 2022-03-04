import pymongo

from cache.decorator import cached, clear_cache
from database.get_db import get_db
from shared.bson_to_json import bson_dumps
from shared.types import Song


class SongController:
    collection_name = 'history'

    def __init__(self):
        self.db = get_db()
        self.collection = self.db.get_collection(self.collection_name)

    @clear_cache('current_song')
    def add_to_history(self, song: Song):
        return self.collection.insert_one(song.to_dict())

    @cached('current_song', data_formatter=bson_dumps, parse_json=True)
    def get_current_song(self):
        return self.collection.find_one(sort=[('timestamp', pymongo.DESCENDING)])

    @cached('last_song', data_formatter=bson_dumps, parse_json=True)
    def get_last_song(self):
        requests = self.collection.find(sort=[('timestamp', pymongo.DESCENDING)]).limit(2)

        return dict(list(requests)[1])
