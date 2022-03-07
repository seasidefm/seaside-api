from secrets import token_hex
from dotenv import load_dotenv

from database.get_db import get_db

deployments = ['botsuro', 'heat-level', 'song-watcher', 'heat-updater', 'testing']

if __name__ == '__main__':
    load_dotenv()
    collection = get_db("token-creator").get_collection('tokens')

    print(f"Creating access tokens for {len(deployments)} deployments")
    for dep in deployments:
        print(f"Name: {dep}")
        token = token_hex(nbytes=16)
        collection.insert_one({
            "name": dep,
            "token": token
        })
        print("...OK")
