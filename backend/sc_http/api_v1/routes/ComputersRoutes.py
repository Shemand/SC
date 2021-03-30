import json

from backend.sc_actions.computers import get_computers, get_or_create_computer
from backend.sc_entities.Entities import Entities
from .BlueprintAttacher import BlueprintAttacher


class ComputersRoutes(BlueprintAttacher):
    def __init__(self, mod, base_name):
        super().__init__(mod, base_name)

    def _attach(self, route):

        @route('/', methods=['GET'])
        def get_computers_info(res):
            """Function for getting all information about computer"""
            district = Entities().get_district(res.district.name)
            database = district.database
            print(get_or_create_computer(database, 'SZO-ASTRA-GLOG'))
            return f'hello world'

        @route('/<computer_id>/comment/', methods=['PUT'])
        def set_computer_comment(res):
            """Function for changing comment of computer"""
            return '{}'

        @route('<computer_name>/type/<type>', methods=['PUT'])
        def change_computer_type(res):
            """Function for changing type of computer(ARM, Server)"""
            return '{}'

        @route('/<computer_name>/lock', methods=['PUT'])
        def lock_computer(res):
            """Function for locking computer by computer_name"""
            return '{}'

        @route('/<computer_name>/unlock', methods=['PUT'])
        def unlock_computer(res):
            """Function for unlocking computer by computer_name"""
            return '{}'
