from dotenv import load_dotenv

from database.get_db import get_db

load_dotenv()
db = get_db()


def build_fave_objects(user: dict):
    fave_objects = []
    for song in user['songs']:
        fave_objects.append({
            "user": user['user'],
            "twitch_id": user.get("twitch_id", ""),
            "date": song['date'],
            "song": song['song']
        })
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

    print("Getting current user objects")
    users = list(users_collection.find())
    print("...OK")

    print("Formatting song objects")
    songs = flatten(list(map(build_fave_objects, users)))
    print("...OK")

    print(f"Migrating {len(songs)} documents to new collection")
    faves_collection.insert_many(songs)
    print("...OK")


