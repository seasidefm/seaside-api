from datetime import datetime
from typing import NewType

SongRequest = NewType('SongRequest', dict)
UserPayload = NewType('UserPayload', dict)

class Request:
    def __init__(self, user="", user_id="", artist="", song_title="", ripped=False, streamed=False, stream_date="", owned=False, timestamp=None) -> None:
        # Legacy requests have username only
        self.user = user
        self.user_id = user_id
        self.artist = artist
        self.song_title = song_title
        self.ripped = ripped
        # Legacy requests have streamed = 1
        self.streamed = streamed or streamed == 1
        self.stream_date = datetime.fromisoformat(stream_date)
        self.timestamp =  datetime.fromisoformat(stream_date) if timestamp else datetime.now()

    def to_dict(self):
        return {
            "user": self.user,
            "user_id": self.user_id,
            "artist": self.artist,
            "song_title": self.song_title,
            "ripped": self.ripped,
            "streamed": self.streamed,
            "stream_date": self.stream_date.isoformat(),
            "timestamp": self.timestamp.isoformat()
        }



class Fave:
    def __init__(self, user: str, song: str, date=None):
        self.user = user
        self.song = song
        self.timestamp = date or datetime.now()

    def to_dict(self):
        return {
            "song": self.song,
            "user_id": self.user,
            "timestamp": self.timestamp.isoformat()
        }


class Song:
    splitter = " - "

    def __init__(self, song: str, date=None):
        # Sanitize every input, as new history inputs may contain newlines!
        song.replace('\n', ' - ')

        # Continue as usual
        artist, song_title = song.split(Song.splitter, maxsplit=1)
        self.song = song_title
        self.artist = artist
        self.timestamp = date or datetime.now()

    def to_dict(self):
        return {
            "song": self.song,
            "artist": self.artist,
            "timestamp": self.timestamp
        }

    def to_song_string(self):
        return f"{self.artist}{Song.splitter}{self.song}"

    @staticmethod
    def from_bson(cached: dict):
        return Song(f"{cached.get('artist')}{Song.splitter}{cached.get('song')}", date=cached.get('timestamp')['$date'])
