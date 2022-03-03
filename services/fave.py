from controllers.fave import FaveController
from controllers.song import SongController
from services.song import SongService


class FaveService:
    """
    This fave service acts as the glue to connect the fave controller
    (or interactor) with other elements related to favorite songs.

    For example, this taps into the song controller in order to pull
    currently playing songs, last played songs, etc.
    """
    def __init__(self):
        self.fave_controller = FaveController()
        self.song_controller = SongController()
        self.song_service = SongService()

    def save_song(self):
        song = self.song_controller.get_current_song()
        print(song)
