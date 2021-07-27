import json

from flask import g, request

from ....sc_actions.computers import get_computers, get_or_create_computer
from ....sc_actions.computers_frame import get_computers_frame, FROM_ACTIVE_DIRECTORY, FROM_PUPPET, FROM_KASPERSKY, FROM_DALLAS_LOCK
from ....sc_actions.functions import rows_to_dicts
from ....sc_actions.kaspersky import update_computers_from_kaspersky
from ....sc_entities.Entities import Entities
from ..functions import required_auth


def attach_computer_routes(mod):

    @mod.route('/<district_name>/computers', methods=['GET'])
    @required_auth
    def get_computers_info(district_name):
        """Function for getting all information about computer"""
        res = g.response
        units = res.user.available_units
        args = request.args
        puppet = args['puppet'] if 'puppet' in args else None
        active_directory = args['active_directory'] if 'active_directory' in args else None
        dallas_lock = args['dallas_lock'] if 'dallas_lock' in args else None
        kaspersky = args['kaspersky'] if 'kaspersky' in args else None
        sources = {}
        if puppet:
            sources[FROM_PUPPET] = json.loads(puppet)
        if active_directory:
            sources[FROM_ACTIVE_DIRECTORY] = json.loads(active_directory)
        if kaspersky:
            sources[FROM_KASPERSKY] = json.loads(kaspersky)
        if dallas_lock:
            sources[FROM_DALLAS_LOCK] = json.loads(dallas_lock)
        data = get_computers_frame(res.database,
                                   units,
                                   sources=sources)
        res.set_data('computers', data)
        return res.success().get()

    @mod.route('/<district_name>/computers/<computer_id>/comment', methods=['GET'])
    def set_computer_comment(district_name, computer_id):
        """Function for changing comment of computer"""
        return '{}'

    @mod.route('/<district_name>/computers/<computer_name>/type/<type>', methods=['PUT'])
    def change_computer_type(district_name, computer_name, type):
        """Function for changing type of computer(ARM, Server)"""
        return '{}'

    @mod.route('/<district_name>/computers/<computer_name>/lock', methods=['PUT'])
    def lock_computer(district_name, computer_name):
        """Function for locking computer by computer_name"""
        return '{}'

    @mod.route('/<district_name>/computers/<computer_name>/unlock', methods=['PUT'])
    def unlock_computer(district_name, computer_name):
        """Function for unlocking computer by computer_name"""
        return '{}'
