from flask import request

from controllers.token import token_required
from shared.structures import AppResult, AppError
from utils.heat_setter import update_heat
from . import blueprint, service_locator


def fave_route(route: str):
    return f"/faves{route}"


@blueprint.post("/songs/new")
@token_required
@update_heat
def new_song():
    data = request.json

    response = None
    try:
        if data['song']:
            result = service_locator.songs.add_current_song(data['song'])
            response = AppResult(
                message=f"Added {data['song']} to history",
                data=result
            )
        else:
            response = AppError(
                message="Song key is missing or incorrect format",
                error="`song` key is required!",
                code=400
            )
    except Exception as e:
        response = AppError(
            message="Something went wrong",
            error=str(e),
            code=500
        )

    return response.response_tuple()

@blueprint.get("/songs/current")
def current_song():
    return AppResult(
        message="Current song",
        data=service_locator.songs.current_song().to_dict()
    ).response_tuple()
