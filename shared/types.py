from datetime import datetime
from typing import NewType

SongRequest = NewType('SongRequest', dict)
UserPayload = NewType('UserPayload', dict)


class Fave:
    def __init__(self, user: str, song: str, date=datetime.now()):
        self.user = user
        self.song = song
        self.timestamp = date

    def to_dict(self):
        return {
            "song": self.song,
            "user_id": self.user,
            "timestamp": self.timestamp.isoformat()
        }


class Song:
    def __init__(self, song: str, date=datetime.now().isoformat()):
        artist, song_title = song.split(' - ')
        self.song = song_title
        self.artist = artist
        self.timestamp = date

    def to_dict(self):
        return {
            "song": self.song,
            "artist": self.artist,
            "timestamp": self.timestamp
        }

    def to_song_string(self):
        return f"{self.artist} - {self.song}"

    @staticmethod
    def from_cache(cached: dict):
        print(cached.get('timestamp')['$date'])
        return Song(f"{cached.get('artist')} - {cached.get('song')}", date=cached.get('timestamp')['$date'])
