import json

import requests

from ..sc_common.functions import reformat_computer_name, extract_unit_from_name
from .ServiceAbstract import ServiceAbstract


class PuppetService(ServiceAbstract):

    def __init__(self, district, main_config, specific_data) -> None:
        super().__init__(district, main_config, specific_data)
        self.fields = specific_data['fields']
        self.unit_prefixes = specific_data['prefixes']

    def create_connection(self):
        pass

    def check_connection(self) -> bool:
        req = requests.get(self._get_address_of_root())
        if req.status_code == 200:
            return True
        return False

    def _get_address_of_root(self):
        return f'http://{self.ip}:{self.port}/'

    def _get_address_of_query(self):
        base_query_string = f'http://{self.ip}:{self.port}/pdb/query/v4/facts?query=["or",'
        base_query_string += '["=", "name", "hostname"]'
        for field_name in self.fields:
            base_query_string += ','
            base_query_string += f'["=", "name", "{field_name}"]'
        base_query_string += ']'
        return base_query_string

    def __get_facts(self):
        if not self.check_connection():
            return []
        req = requests.get(self._get_address_of_query())
        data = req.content
        data = json.loads(data)
        if req.status_code == 200:
            return data
        else:
            return []

    def _format_records(self, records):
        fields = ['environment, cert_name'].extend(self.fields)
        for computer_name, record in records.items():
            for field_name in self.fields:
                if not field_name in record:
                    record[field_name] = None

    def get_computers(self):
        records = self.__get_facts()
        computers = {}
        for record in records:
            computer_name = reformat_computer_name(record['certname'])
            unit_name = extract_unit_from_name(computer_name)
            if not unit_name in self.unit_prefixes:
                continue
            cert_name, env, name, value = record['certname'], record['environment'], record['name'], record['value']
            if not computer_name in computers:
                computers[computer_name] = {
                    'environment': env,
                    'cert_name' : cert_name
                }
            if name in computers[computer_name]:
                print(f'{name} already exist in computers - {computer_name}')
            if computers[computer_name]['environment'] != env:
                print(f'{computer_name} not equal declared before')
            computers[computer_name][name] = value
        self._format_records(computers)
        return computers