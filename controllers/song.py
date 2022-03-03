from cache.decorator import cached
from database.get_db import get_db
from shared.bson_to_json import bson_to_dict, bson_dumps


class SongController:
    def __init__(self):
        self.db = get_db()
        self.PLAYLIST_COLLECTION = 'current_song'

    @cached('current_song', data_formatter=bson_dumps, parse_json=True)
    def get_current_song(self):
        collection = self.db.get_collection(self.PLAYLIST_COLLECTION)
        requests = collection.find({"type": "current_song"})

        return dict(list(requests)[0])

    @cached('last_song', data_formatter=bson_dumps, parse_json=True)
    def get_last_song(self):
        collection = self.db.get_collection(self.PLAYLIST_COLLECTION)
        requests = collection.find({"type": "last_song"})

        return dict(list(requests)[0])
