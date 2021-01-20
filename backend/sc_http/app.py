from flask import Blueprint, g, request, session
from .ApiComputersRoutes import ApiComputersRoutes
from ...sc_entities.RequrestTuner import RequestTuner

mod = Blueprint('api', __name__, url_prefix='/api/')

@mod.before_request
def attach_tuner():
    if 'user_id' in session and 'district_name' in session:
        g.loggined = True
        g.user = None
        g.district = None
        g.user_role = None
    else:
        g.loggined = False

ApiComputersRoutes(mod, 'computers')