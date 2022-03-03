import json

from bson import json_util


def bson_to_json(data):
    return json.loads(json_util.dumps(data))
