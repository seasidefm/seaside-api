from json import loads
from bson.json_util import dumps
from controllers.request import RequestController
from shared.bson_utils import bson_to_list


class RequestService:
    def __init__(self):
        self.request_controller = RequestController()
    
    def get_requests(self) -> list:
        return bson_to_list(self.request_controller.get_requests())