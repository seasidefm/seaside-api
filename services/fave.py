from controllers.fave import FaveController
from controllers.song import SongController


class FaveService:
    def __init__(self):
        self.fave_controller = FaveController()
        self.song_controller = SongController()

    def save_song(self):
        song = self.song_controller.get_current_song()
        print(song)
