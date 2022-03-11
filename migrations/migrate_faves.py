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


def build_superfave_object(old: dict):
    print(old)
    new = Fave(
        old.get('twitch_id'),
        old.get('song').strip(),
        date=datetime.datetime.fromtimestamp(old.get('date'))
    ).to_dict()
    print(new)
    return new


def flatten(data: list):
    flat_list = []
    for sublist in data:
        for item in sublist:
            flat_list.append(item)

    return flat_list


if __name__ == "__main__":
    print("Running migration script")
    users_collection = db.get_collection("saved_songs")
    new_faves_collection = db.get_collection("favorites")

    old_superfaves = db.get_collection('super_faves')
    new_superfaves = db.get_collection("superfaves")

    print("Dropping existing new collections")
    new_faves_collection.delete_many({})
    new_superfaves.delete_many({})
    print("...OK")

    print("Getting current user objects")
    users = list(users_collection.find({}))
    print("...OK")

    print("Formatting song objects")
    new_fave_documents = flatten(list(map(build_fave_objects, users)))
    print("...OK")

    print("Getting current superfaves")
    old_superfave_documents = list(old_superfaves.find({}))
    print("...OK")

    print("Formatting superfave objects")
    new_superfave_documents = list(map(build_superfave_object, old_superfave_documents))
    print(new_superfave_documents)
    print("...OK")

    print(f"Migrating {len(new_fave_documents) + len(new_superfave_documents)} documents to new collection")
    print("First migrating faves...")
    new_faves_collection.insert_many(new_fave_documents)
    print("Now migrating superfaves...")
    new_superfaves.insert_many(new_superfave_documents)
    print("...OK")


