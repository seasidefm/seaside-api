from controllers.fave import FaveController
from controllers.song import SongController
from shared.types import Song, Fave


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

    def save_song(self, user: str):
        song = Song.from_bson(self.song_controller.get_current_song())
        fave = Fave(user, song.to_song_string())

        return self.fave_controller.add_fave(fave=fave)
