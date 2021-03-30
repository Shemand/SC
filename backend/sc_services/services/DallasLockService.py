import json

import requests

from backend.sc_services.services.ServiceAbstract import ServiceAbstract


class DallasLockService(ServiceAbstract):

    def __init__(self, configurations: dict) -> None:
        super().__init__(configurations['name'], configurations)
        self._ip = configurations['ip']
        self._port = configurations['port']
        self._server = configurations['server']

    def create_connection(self):
        pass

    def check_connection(self) -> bool:
        pass

    def _get_address_of_tree(self):
        return f'http://{self._ip}:{self._port}/tree'

    def __get_computers_raw(self):
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
            "server" : record['server'],
            "name" : record['computer'],
            "container" : record['nodes'].pop(len(record['nodes']) - 1),
            "status" : record['status']
        } for record in records]
        for computer in computers:
            index = computer['name'].find('[')
            if index != -1:
                computer['name'] = computer['name'][0:index].strip()
        return computers