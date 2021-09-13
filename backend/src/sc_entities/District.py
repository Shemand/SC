import json
import os
from os.path import join as join_path

from ..sc_repositories.DatabaseRepository import DatabaseRepository
from .CryptoGateway import CryptoGateway
from .DistrictServices import DistrictServices
from .DistrictUnit import DistrictUnit
from ..sc_repositories.ActiveDirectoryRepository import ActiveDirectoryRepository
from ..sc_repositories.ServiceFactory import ServiceFactory

SERVICES = 'services.json'
UNITS = 'new_unit.json'
MAIN = 'main.json'
DATABASE = 'database.json'
STRUCTURE = 'structure.json'
NEW_UNITS = 'new_unit.json'
CRYPTO_GATEWAYS = 'crypto_gateways.txt'
JSON_CONFIG_NAMES = [NEW_UNITS, SERVICES, UNITS, MAIN, DATABASE]
CSV_CONFIG_NAMES = [CRYPTO_GATEWAYS]

class District:

    def __init__(self, district_name):
        self.name = district_name
        self._structure = self.__extract_structures(self.__read_json_config(NEW_UNITS))
        self._services = self.__load_services(self.__read_json_config(SERVICES))
        self._units = self.__load_units(self.__read_json_config(UNITS))
        self._main = self.__read_json_config(MAIN)
        self._database = self.__load_database(self.__read_json_config(DATABASE))
        self._crypto_gateways = self.__load_crypto_gateways(self.__read_csv_config(CRYPTO_GATEWAYS, '/'))
        self.__appoint_cg_to_units()

# -------- PROPERTIES -----------

    @property
    def services(self):
        return self._services

    @property
    def units(self):
        return self._units

    @property
    def database(self):
        return self._database

    @property
    def crypto_gateways(self):
        return self._crypto_gateways

    @property
    def structure(self):
        return self._structure

# -------- PUBLIC ---------------

    def get_available_containers(self, container_name):
        return self._get_available_containers(container_name, self._structure)

    def get_available_units(self, unit_name):
        return {name : unit for name, unit in self.units.items()
                if name in self._get_available_containers(unit_name)}

    def get_active_directory_services(self):
        return [service for service in self.services if isinstance(service, ActiveDirectoryRepository)]
# -------- READERS --------------

    def __read_json_config(self, config_name):
        assert config_name in JSON_CONFIG_NAMES, 'Unknown config_type in __read_json_config'
        file = open(self.get_file_path(config_name), 'r')
        information = file.read()
        information = json.loads(information)
        return information

    def __read_csv_config(self, config_name, spliter='/'):
        assert config_name in CSV_CONFIG_NAMES, 'Unknown config_type in __read_csv_config'
        file = open(self.get_file_path(config_name), 'r')
        information = []
        for line in file:
            parts = line.split(spliter)
            information.append(parts)
        return information

# -------- PRIVATE --------------

    def get_file_path(self, config_name):
        path = os.getcwd()
        path = join_path(path, 'configs')
        path = join_path(path, 'districts')
        path = join_path(path, self.name)
        return join_path(path, config_name)

    def __appoint_cg_to_units(self):
        for cg_name in self._crypto_gateways:
            cg = self._crypto_gateways[cg_name]
            assert cg.unit in self._units, f'__Appoint_cg_to_units. CryptoGateway ({cg.name}) have not existing unit ({cg.unit})'
            self._units[cg.unit].append_crypto_gateway(cg)

    def __prepare_service_data(self, service):
        settings = {
            "name": service['connection_name'],
            "ip": service['connection_ip'],
            "port": service['connection_port']
        }
        specific_data = service['specific_data']
        if service['type'] == DistrictServices.AD:
            settings['username'] = specific_data['username']
            settings['password'] = specific_data['password']
            settings['path'] = specific_data['main_container_path']
            settings['begin_node'] = specific_data['begin_node']
            settings['end_nodes'] = specific_data['end_nodes']
        elif service['type'] == DistrictServices.DALLAS:
            settings['server'] = specific_data['server']
        elif service['type'] == DistrictServices.KASPERSKY:
            settings['username'] = specific_data['username']
            settings['password'] = specific_data['password']
            settings['server'] = specific_data['server']
        else:
            assert False, f'Unknown DistinctServices.TYPE in service with name: "{service["connection_name"]}"'
        return settings

    def _get_available_containers(self, container_name, root_children, flag=False):
        available_containers = []
        for unit_name, children in root_children.items():
            if unit_name == container_name:
                flag = True
            if flag:
                available_containers.append(unit_name)
            if children != {}:
                available_containers.extend(self._get_available_containers(container_name, children, flag))
        return available_containers

# -------- LOADRES --------------

    def __extract_structures(self, units):
        root_units = {}
        for unit_name, values in units.items():
            if values['children'] != {}:
                root_units[unit_name] = self.__extract_structures(values['children'])
            else:
                root_units[unit_name] = {}
        return root_units

    def __load_units(self, config_dict):
        units_objects = {}
        for unit_name, data in config_dict.items():
            if data['children'] != {}:
                units_objects = {**units_objects, **self.__load_units(data['children'])}
            units_objects[unit_name] = DistrictUnit(self, unit_name, config_dict[unit_name])
        return units_objects

    def __load_services(self, config_dict):
        district_services = DistrictServices(self.name)
        for service in config_dict:
            if service['active'] == False:
                continue
            district_services.add_service(ServiceFactory.create_service(self, service))
        return district_services

    def __load_database(self, config_dict):
        return DatabaseRepository(database_config=config_dict)

    def __load_crypto_gateways(self, crypto_gateways):
        district_cg = {}
        for cg in crypto_gateways:
            if cg[5] == '-':
                continue
            information = {
                "address" : cg[0],
                "mask" : cg[1],
                "unit" : cg[2],
                "caption" : cg[3],
                "name" : cg[4]
            }
            district_cg[ information['name'] ] = CryptoGateway(self,
                                                               information['name'],
                                                               information)
        return district_cg

# --------- MAGIC METHODS ------------

    def __getitem__(self, unit_name):
        return self.units[unit_name]

    def __repr__(self):
        return f'<District (name: {self.name})>'