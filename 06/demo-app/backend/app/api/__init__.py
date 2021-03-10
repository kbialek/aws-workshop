from flask import Blueprint

api = Blueprint('api', __name__)

from . import vehicles_model
from . import vehicles_controller

from . import metadata_controller
from . import healthcheck_controller
