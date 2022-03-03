from database.get_db import get_db


class FaveController:
    def __init__(self):
        self.db = get_db()

    def test(self):
        print("test")
