import json

from bson import json_util


def bson_dumps(data):
    return json_util.dumps(data)


def bson_to_dict(data):
    return json.loads(json_util.dumps(data))
