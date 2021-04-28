import json

import requests

from backend.sc_common.functions import reformat_computer_name
from backend.sc_services.ServiceAbstract import ServiceAbstract


class DallasLockService(ServiceAbstract):

    def __init__(self, district, main_config, specific_data) -> None:
        super().__init__(district, main_config, specific_data)
        self.server = self.configuration['server']

    def create_connection(self):
        pass

    def check_connection(self) -> bool:
        req = requests.get(self._get_address_of_tree(), timeout=30)
        if req.status_code == 200:
            return True
        return False

    def get_address_of_root(self):
        return f'http://{self._ip}:{self._port}/'

    def _get_address_of_tree(self):
        return f'http://{self._ip}:{self._port}/tree'

    def __get_computers_raw(self):
        assert self.check_connection(), f'Server ({self._ip}:{self._port}) is not available now.'
        req = requests.get(self._get_address_of_tree())
        data = req.content
        data = json.loads(data)
        if req.status_code == 200:
            return data
        else:
            return []

    def get_computers(self):
        records = self.__get_computers_raw()
        computers = [{
            "server": record['server'],
            "name": reformat_computer_name(record['computer']),
            "container": record['nodes'].pop(len(record['nodes']) - 1),
            "status": record['status']
        } for record in records]
        for computer in computers:
            index = computer['name'].find('[')
            if index != -1:
                computer['name'] = computer['name'][0:index].strip()
        return computers
