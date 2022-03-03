from cache.cache import Cache
from controllers.song import SongController


class SongService:
    def __init__(self):
        self.song_collection = SongController()
        self.cache = Cache()

    def current_song(self):
        return self.song_collection.get_current_song()

    def last_song(self):
        return self.song_collection.get_last_song()
