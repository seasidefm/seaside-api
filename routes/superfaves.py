from flask import request

from shared.structures import AppResult
from . import blueprint, service_locator


@blueprint.get("/superfaves")
def superfaves_for_user():
    user = request.args.get('user_id')
    return AppResult(
        message="User's superfave songs",
        data=service_locator.superfaves.get_songs(user)
    ).response_tuple()
