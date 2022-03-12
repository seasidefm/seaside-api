from controllers.superfave import SuperfaveController
from services.fave import FaveService


class SuperFaveService(FaveService):
    def __init__(self):
        super().__init__()
        self.fave_controller = SuperfaveController()
