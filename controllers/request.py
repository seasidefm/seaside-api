from typing import List
from database.get_db import get_db
from shared.bson_utils import bson_dumps
from shared.types import Request


class RequestController:
    collection_name = 'requests'

    def __init__(self):
        db = get_db("request-controller")
        self.collection = db.get_collection(self.collection_name)

    def get_requests(self):
        return self.collection.find({})

    def get_user_requests(self, user_id: str):
        return self.collection.find({ user_id })