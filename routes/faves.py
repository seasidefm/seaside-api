from flask import request

from shared.structures import AppResult
from . import blueprint, service_locator


def fave_route(route: str):
    return f"/faves{route}"


@blueprint.get(fave_route("/user"))
def faves_for_user():
    user = request.args.get('user_id')
    return AppResult(
        message="User's favorite songs",
        data=service_locator.faves.get_songs(user)
    ).response_tuple()
