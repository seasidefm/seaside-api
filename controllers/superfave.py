from cache.cache_decorator import cached
from controllers.fave import FaveController
from database.aggregates import all_songs_ranked, SUPERFAVE_SCORE
from shared.bson_utils import bson_dumps


class SuperfaveController(FaveController):
    collection_name = 'superfaves'
    points_per_fave = SUPERFAVE_SCORE
