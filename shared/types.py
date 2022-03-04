from datetime import datetime
from typing import NewType

SongRequest = NewType('SongRequest', dict)
UserPayload = NewType('UserPayload', dict)


class Song:
    def __init__(self, song: str, date=None):
        artist, song_title = song.split(' - ')
        self.song = song_title
        self.artist = artist
        self.timestamp = date if date is not None else datetime.now()

    def to_dict(self):
        return {
            "song": self.song,
            "artist": self.artist,
            "timestamp": self.timestamp
        }
