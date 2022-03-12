from flask import request

from controllers.token import token_required
from shared.structures import AppResult, AppError
from utils.heat_setter import update_heat
from . import blueprint, service_locator


@blueprint.get("/superfaves")
def superfaves_for_user():
    user = request.args.get('user_id')
    return AppResult(
        message="User's superfave songs",
        data=service_locator.superfaves.get_songs(user)
    ).response_tuple()


@blueprint.delete("/superfaves")
@token_required
@update_heat
def delete_superfave():
    data = request.json
    fave_id = data.get('fave_id')

    response = None
    if fave_id:
        result = service_locator.superfaves.delete_fave(fave_id)
        if result:
            response = AppResult(message="Superfave successfully deleted", data={
                "data": True
            })
        else:
            response = AppError(
                message="Something went wrong deleting superface!",
                error="Could not delete superfave, please check ID"
            )
    else:
        response = AppError(
            message="Fave ID is missing from request body",
            error="`fave_id` is missing or improper format",
            code=400
        )

    return response.response_tuple()
