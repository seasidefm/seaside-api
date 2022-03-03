from database.get_db import get_db


class SongController:
    def __init__(self):
        self.db = get_db()
        self.PLAYLIST_COLLECTION = 'current_song'

    def get_current_song(self):
        collection = self.db.get_collection(self.PLAYLIST_COLLECTION)
        requests = collection.find({"type": "current_song"})

        return dict(list(requests)[0])

    def get_last_song(self):
        collection = self.db.get_collection(self.PLAYLIST_COLLECTION)
        requests = collection.find({"type": "last_song"})

        return dict(list(requests)[0])