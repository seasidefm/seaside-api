from shared.structures import AppResponse
from . import blueprint


def leaderboard_route(route: str):
    return f"/leaderboards{route}"


@blueprint.get(leaderboard_route('/top-songs'))
def top_songs():
    return AppResponse(
        data=[],
        message="Current top songs"
    ).response_tuple()
