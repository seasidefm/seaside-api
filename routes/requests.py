from shared.structures import AppResult
from . import blueprint, service_locator

@blueprint.get('/requests')
def get_requests():
    return AppResult(
        message="All user requests",
        data=service_locator.requests.get_requests()
    ).response_tuple()
