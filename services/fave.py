from controllers.fave import FaveController
from controllers.song import SongController
from shared.bson_utils import bson_to_list
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

    def count(self, song: str):
        return self.fave_controller.get_count(song)

    def save_song(self, user: str):
        song = Song.from_bson(self.song_controller.get_current_song())
        fave = Fave(user, song.to_song_string())

        return self.fave_controller.add_fave(fave=fave)

    def save_last(self, user: str):
        song = Song.from_bson(self.song_controller.get_last_song())
        fave = Fave(user, song.to_song_string())

        return self.fave_controller.add_fave(fave=fave)

    def delete_fave(self, fave_id: str):
        result = self.fave_controller.del_fave(fave_id)

        return result.deleted_count > 0

    def get_songs(self, user_id: str, limit=0):
        return bson_to_list(list(self.fave_controller.get_faves_for_user(user_id, limit=limit)))
