from shared.structures import AppResponse
from . import blueprint, service_locator


def leaderboard_route(route: str):
    return f"/leaderboards{route}"


@blueprint.get(leaderboard_route('/top-songs'))
def top_songs():
    service = service_locator.leaderboard

    return AppResponse(
        data=service.get_fave_points(),
        message="Current top songs"
    ).response_tuple()
