from shared.structures import AppResult
from . import blueprint, service_locator

@blueprint.get('/heat')
def get_heat():
    return AppResult(
        message="Current heat level",
        data=service_locator.heat.get_current_heat()
    ).response_tuple()
