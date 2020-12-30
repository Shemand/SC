from flask import Blueprint, g, request
from .ApiComputersRoutes import ApiComputersRoutes
from ...sc_entities.RequrestTuner import RequestTuner

mod = Blueprint('api', __name__, url_prefix='/api/')

@mod.before_request
def attach_tuner():
    RequestTuner(g, request)

ApiComputersRoutes(mod, 'computers')


