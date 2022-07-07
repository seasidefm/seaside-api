import os
from pymongo import MongoClient


class Database:
    def __init__(self):
        connection_string = os.environ.get('MONGO_CONNECTION')
        if not connection_string:
            raise EnvironmentError("MONGO_CONNECTION missing in env!")

        self.mongo = MongoClient(connection_string)
        self.db = self.mongo.get_default_database()

    def instance(self):
        return self.db


db = None


def get_db(service: str):
    global db
    if db is None:
        print(f'[{service}] Database connection is None, initializing...')
        db = Database()
        return db.instance()
    else:
        print(f'[{service}] Reusing existing database connection')
        return db.instance()
