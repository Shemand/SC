from flask import Blueprint
from .ApiComputersRoutes import ApiComputersRoutes

mod = Blueprint('api', __name__, url_prefix='/api/')

ApiComputersRoutes(mod, 'computers')


