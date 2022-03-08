from controllers.superfave import SuperFaveController
from services.fave import FaveService


class SuperFaveService(FaveService):
    def __init__(self):
        super().__init__()
        self.fave_controller = SuperFaveController()
