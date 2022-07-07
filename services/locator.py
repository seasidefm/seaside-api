from services.fave import FaveService
from services.heat import HeatService
from services.leaderboard import LeaderboardService
from services.request import RequestService
from services.song import SongService
from services.superfave import SuperFaveService
from services.video import VideoInfoService


class Locator:
    """
    The Service Locator class is designed to ease the pain of importing
    tens of services or trying to decide what you do or don't need.

     Instead of importing two or three services, you can instead import ONE
     service, and use dot notation to access others :)
    """
    def __init__(self):
        self.videos = VideoInfoService()
        self.faves = FaveService()
        self.superfaves = SuperFaveService()
        self.leaderboard = LeaderboardService()
        self.requests = RequestService()
        self.songs = SongService()
        self.heat = HeatService()
