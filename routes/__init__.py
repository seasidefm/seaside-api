from flask import Blueprint

from services.locator import Locator

blueprint = Blueprint('seaside-blueprint', __name__)

service_locator = Locator()

from . import faves
from . import leaderboards
