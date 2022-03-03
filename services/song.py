from controllers.song import SongController
from shared.bson_to_json import bson_to_json


class SongService:
    def __init__(self):
        self.song_collection = SongController()

    def current_song(self):
        song = self.song_collection.get_current_song()
        return bson_to_json(song)

    def last_song(self):
        song = self.song_collection.get_last_song()
        return bson_to_json(song)
