from shared.structures import AppResponse
from . import blueprint, service_locator


def leaderboard_route(route: str):
    return f"/leaderboards{route}"


@blueprint.get(leaderboard_route('/faves'))
def top_faves():
    service = service_locator.leaderboard

    return AppResponse(
        data=service.get_fave_points(),
        message="Current top songs"
    ).response_tuple()


@blueprint.get(leaderboard_route('/superfaves'))
def top_superfaves():
    service = service_locator.leaderboard

    return AppResponse(
        data=service.get_superfave_points(),
        message="Current top songs"
    ).response_tuple()


@blueprint.get(leaderboard_route('/top-songs'))
def top_songs():
    service = service_locator.leaderboard

    return AppResponse(
        data=service.get_total_points(),
        message="Current top songs"
    ).response_tuple()


@blueprint.get(leaderboard_route('/user-points'))
def user_points():
    service = service_locator.leaderboard

    return AppResponse(
        data=service.get_user_faves(),
        message="Current top users"
    ).response_tuple()
