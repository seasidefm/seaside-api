from flask import request

from controllers.token import token_required
from shared.structures import AppResult, AppError
from utils.heat_setter import update_heat
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

@blueprint.post("/faves")
@token_required
@update_heat
def new_fave():
    data = request.json

    response = None
    user_id = data.get('user_id')
    song = data.get('song')
    if user_id:
        result =\
            service_locator.faves.save_last(user_id)\
            if song == "last" else\
            service_locator.faves.save_song(user_id)

        if result:
            response = AppResult(
                message="Added current song as favorite",
            )

        else:
            response = AppError(
                message="Already user favorite",
                error=f"Already a favorite for {user_id}",
                code=409
            )
    else:
        response = AppError(
            message="User ID key is missing or wrong format",
            error="`user_id` key is required to favorite current song",
            code=400
        )

    return response.response_tuple()
