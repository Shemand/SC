import json

from flask import g, Blueprint

from ..handlers.ComputersHandlers import get_computers_info_handler, lock_computer_handler, \
    change_computer_type_handler, unlock_computer_handler, set_computer_comment_handler
from ...sc_services.ComputersService import get_computers, get_or_create_computer
from ...sc_services.ComputersFrameService import get_computers_frame, FROM_ACTIVE_DIRECTORY, FROM_PUPPET, FROM_KASPERSKY, FROM_DALLAS_LOCK
from ...sc_common.functions import rows_to_dicts
from ...sc_services.KasperskyService import update_computers_from_kaspersky
from ...sc_entities.Entities import Entities
from ..functions import required_auth

mod = Blueprint('computers', __name__, url_prefix='/computers/')


@mod.route('/', methods=['GET'])
@required_auth
def get_computers_info(district_name):
    middleware = g.middleware
    return get_computers_info_handler(middleware)


@mod.route('/<computer_id>/comment', methods=['GET'])
def set_computer_comment(computer_id):
    middleware = g.middleware
    return set_computer_comment_handler(middleware, computer_id)


@mod.route('/<computer_name>/type/<type>', methods=['PUT'])
def change_computer_type(computer_name, type):
    middleware = g.middleware
    return change_computer_type_handler(middleware, computer_name, type)


@mod.route('/<computer_name>/lock', methods=['PUT'])
def lock_computer(computer_name):
    middleware = g.middleware
    return lock_computer_handler(middleware, computer_name)


@mod.route('/<computer_name>/unlock', methods=['PUT'])
def unlock_computer(computer_name):
    middleware = g.middleware
    return unlock_computer_handler(middleware, computer_name)
