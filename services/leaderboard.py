from controllers.fave import FaveController
from controllers.superfave import SuperfaveController


class LeaderboardService:
    def __init__(self):
        self.fave_controller = FaveController()
        self.superfave_controller = SuperfaveController()

    def get_fave_points(self):
        return list(self.fave_controller.get_fave_points())

    def get_superfave_points(self):
        return list(self.superfave_controller.get_fave_points())
