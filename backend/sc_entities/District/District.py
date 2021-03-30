import ipaddress
import json
import os
from os.path import join as join_path

from backend.sc_database.database import DatabaseClass
from backend.sc_entities.District.CryptoGateway import CryptoGateway
from backend.sc_entities.District.DistrictServices import DistrictServices
from backend.sc_entities.District.DistrictUnit import DistrictUnit
from backend.sc_services.services.ActiveDirectoryService import ActiveDirectoryService
from backend.sc_services.services.DallasLockService import DallasLockService
from backend.sc_services.services.KasperskyService import KasperskyService

SERVICES = 'services.json'
UNITS = 'units.json'
MAIN = 'main.json'
DATABASE = 'database.json'
CRYPTO_GATEWAYS = 'crypto_gateways.txt'
JSON_CONFIG_NAMES = [SERVICES, UNITS, MAIN, DATABASE]
CSV_CONFIG_NAMES = [CRYPTO_GATEWAYS]

class District:

    def __init__(self, district_name):
        self.name = district_name
        self._services = self.__transformation_data_to_services(self.__read_json_config(SERVICES))
        self._units = self.__transformation_data_to_units(self.__read_json_config(UNITS))
        self._main = self.__read_json_config(MAIN)
        self._database = self.__transformation_data_to_database(self.__read_json_config(DATABASE))
        self._crypto_gateways = self.__transformation_data_to_crypto_gateways(self.__read_csv_config(CRYPTO_GATEWAYS, '/'))
        self.__appoint_cg_to_units()

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

    def get_file_path(self, config_name):
        path = os.getcwd()
        path = join_path(path, 'sc_config')
        path = join_path(path, 'districts')
        path = join_path(path, self.name)
        return join_path(path, config_name)

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

    def __transformation_data_to_units(self, units):
        units_objects = {}
        for unit_name in units:
            units_objects[unit_name] = DistrictUnit(self, unit_name, units[unit_name])
        return units_objects

    def __transformation_data_to_services(self, services):
        district_services = DistrictServices(self.name)
        for service in services:
            if service['active'] == False:
                continue
            settings = self.__prepare_service_data(service)
            district_services.add_service(service['type'], settings)
        return district_services

    def __transformation_data_to_database(self, database):
        return DatabaseClass(database_config=database)

    def __transformation_data_to_crypto_gateways(self, crypto_gateways):
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

    def __getitem__(self, unit_name):
        return self._units[unit_name]

    def __repr__(self):
        return f'<District (name: {self.name})>'