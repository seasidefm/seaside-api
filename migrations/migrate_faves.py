import datetime

from dotenv import load_dotenv

from database.get_db import get_db
from shared.types import Fave

load_dotenv()
db = get_db("migrator")


def build_fave_objects(user: dict):
    fave_objects = []
    for song in user['songs']:
        fave = Fave(
            user.get("twitch_id"),
            song['song'].strip(),
            date=datetime.datetime.fromtimestamp(song.get('date'))
        )
        fave_objects.append(fave.to_dict())
    return fave_objects


def flatten(data: list):
    flat_list = []
    for sublist in data:
        for item in sublist:
            flat_list.append(item)

    return flat_list


if __name__ == "__main__":
    print("Running migration script")
    users_collection = db.get_collection("saved_songs")
    faves_collection = db.get_collection("favorites")

    print("Dropping existing favorites collection")
    # faves_collection.delete_many({})
    print("...OK")

    print("Getting current user objects")
    users = list(users_collection.find({"user": "duke_ferdinand"}))
    print("...OK")

    print("Formatting song objects")
    songs = flatten(list(map(build_fave_objects, users)))
    print("...OK")

    print(f"Migrating {len(songs)} documents to new collection")
    faves_collection.insert_many(songs)
    print("...OK")


