import json

from bson import json_util


def bson_dumps(data):
    return json_util.dumps(data)


def __bson_to_json(data):
    return json.loads(json_util.dumps(data))


def bson_to_dict(data):
    return __bson_to_json(data)


def bson_to_list(data):
    return __bson_to_json(data)
