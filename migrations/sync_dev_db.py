import bson
import pymongo
from pymongo.server_api import ServerApi

db_client = pymongo.MongoClient("mongodb+srv://botsuro:KYZD5TEsGPlxSdTb@botsuro.easqi.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
# current_db = db_client.devDb
# new_prod_db = db_client.prod

collections = [
    'favorites',
    'history',
    'requests',
    'superfaves',
    'tokens'
]

for collection in collections:
    print(f'Migrating {collection}')
    c = current_db.get_collection(collection)
    new_collection = new_prod_db.get_collection(collection)

    documents = list(c.find())
    print(f'Found {len(documents)} documents. Syncing...')
    new_collection.delete_many({})
    new_collection.insert_many(documents)
    print(f'Done!')

