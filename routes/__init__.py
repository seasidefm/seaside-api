from flask import Blueprint

blueprint = Blueprint('seaside-blueprint', __name__)

from . import leaderboards