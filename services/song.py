from cache.cache import Cache
from controllers.song import SongController
from shared.types import Song


class SongService:
    def __init__(self):
        self.song_collection = SongController()
        self.cache = Cache()

    def add_current_song(self, song: str):
        _song = Song(song)
        self.song_collection.add_to_history(_song)
        return "OK"

    def current_song(self):
        return self.song_collection.get_current_song()

    def last_song(self):
        return self.song_collection.get_last_song()
