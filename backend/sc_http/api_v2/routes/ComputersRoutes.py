import json

from flask import g

from backend.sc_actions.computers import get_computers, get_or_create_computer
from backend.sc_actions.functions import rows_to_dicts
from backend.sc_actions.kaspersky import update_computers_from_kaspersky
from backend.sc_entities.Entities import Entities
from backend.sc_http.api_v2.functions import required_auth


def attach_computer_routes(mod):

    @mod.route('/<district_name>/computers', methods=['GET'])
    @required_auth
    def get_computers_info(district_name):
        """Function for getting all information about computer"""
        res = g.response
        data = rows_to_dicts(get_computers(g.response.database))
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
