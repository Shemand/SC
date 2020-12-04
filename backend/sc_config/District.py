import json
import os
from os.path import join as join_path

SERVICES = 'services.json'
UNITS = 'units.json'
MAIN = 'main.json'
CONFIG_NAMES = [SERVICES, UNITS, MAIN]

class DistrictUnit:

    def __init__(self, name, information):
        self.name = name
        self.caption = information['caption']
        self.dallas_containers = information['dallas_containers']
        self.active_directory_containers = information['active_directory_containers']
        self.kaspersky_services_name = information['kaspersky_services']

    def __repr__(self):
        return f'<DistrictUnit (name: {self.name})>'

class District:

    def __init__(self, district_name):
        self.name = district_name
        self._services = self.__read_json_config(SERVICES)
        self._units = self.__transformation_data_of_unit(self.__read_json_config(UNITS))
        self._main = self.__read_json_config(MAIN)

    def get_file_path(self, config_name):
        path = os.getcwd()
        path = join_path(path, 'sc_config')
        path = join_path(path, self.name)
        return join_path(path, config_name)

    def __read_json_config(self, config_name):
        assert config_name in CONFIG_NAMES, 'Unknown config_type in __read_json_config'
        file = open(self.get_file_path(config_name), 'r')
        information = file.read()
        information = json.loads(information)
        return information

    def __transformation_data_of_unit(self, units):
        units_objects = {}
        for unit_name in units:
            units_objects[unit_name] = DistrictUnit(unit_name, units[unit_name])
        return units_objects

    def __getitem__(self, unit_name):
        return self._units[unit_name]

    def __repr__(self):
        return f'<District (name: {self.name})>'