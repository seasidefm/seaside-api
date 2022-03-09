import json

from cache.cache_decorator import cache, cached
from services.fave import FaveService
from services.song import SongService
from services.superfave import SuperFaveService


class HeatService:
    def __init__(self):
        self.song_service = SongService()
        self.fave_service = FaveService()
        self.superfave_service = SuperFaveService()

    def get_heat(self, song: str):
        fave_heat, superfave_heat = [
            self.fave_service.count(song),
            self.superfave_service.count(song)
        ]

        return {
            "heat_level": fave_heat + (superfave_heat * 5)
        }

    @cached('heat', data_formatter=json.dumps, parse_json=True)
    def get_current_heat(self):
        song = self.song_service.current_song()
        return self.get_heat(song.to_song_string())
