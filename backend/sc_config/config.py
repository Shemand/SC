import json
import os

from backend.sc_config.District import District


class Configuration:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configuration, cls).__new__(cls)
            cls.instance.reload()
        return cls.instance

    def reload(self):
        file = open(os.path.join("sc_config","config.json"), 'r')
        configuration = json.loads(file.read())
        self.__districts = configuration['districts']
        self.districts = []
        for district_name in self.__districts:
            self.districts.append(District(district_name))
        self.kaspersky = {
            "win_agent" : configuration['kaspersky']['win_agent_versions'],
            "win_security" : configuration['kaspersky']['win_security_versions'],
            "linux_agent" : configuration['kaspersky']['linux_agent_versions'],
            "linux_security" : configuration['kaspersky']['linux_security_versions'],
            "right_agent" : configuration['kaspersky']['right_agent_versions'],
            "right_security": configuration['kaspersky']['right_security_versions'],
        }

class ServicesConfig:
    def __new__(cls, config: Configuration = None):
        if not hasattr(cls, 'instance'):
            if config is None:
                assert False, 'ServiceConfig need config instance by first execute'
            cls.instance = super(ServicesConfig, cls).__new__(cls)
            cls.instance.reload(config)
        return cls.instance

    def reload(self, config: Configuration = None):
        if config is not None:
            self.config = config
        file = open("sc_config/SZO/services.json", 'r')
        self.__services = json.loads(file.read())
        self.districts_services = {}
        for district in config.districts:
            self.districts_services[district] = {}
            self.districts_services[district]['all'] = {}
        for district_name in self.districts_services:
            self.__load_ad(district_name)
            self.__load_kaspersky(district_name)
            self.__load_dl(district_name)
            self.__load_database(district_name)

    def __load_ad(self, district_name: str) -> None:
        district = self.__get_district(district_name)
        district['ad'] = {}
        for svc in self.__services:
            if svc['active'] and svc['type'] == 'active_directory':
                self.__check_exist(svc['connection_name'])
                district['all'][ svc['connection_name'] ] = {
                    "name" : svc['connection_name'],
                    "ip" : svc['connection_ip'],
                    "port" : svc['connection_port'],
                    "type" : svc['type'],
                    "username" : svc['specific_data']['username'],
                    "password" : svc['specific_data']['password'],
                    "path" : svc['specific_data']['main_container_path'],
                    "begin_node" : svc['specific_data']['begin_node'],
                    "end_nodes" : svc['specific_data']['end_nodes'],
                }
                district['ad'][ svc['connection_name'] ] = district['all'][ svc['connection_name'] ]

    def __load_kaspersky(self, district_name: str) -> None:
        district = self.__get_district(district_name)
        district['kaspersky'] = {}
        for svc in self.__services:
            if svc['active'] and svc['type'] == 'kaspersky':
                self.__check_exist(svc['connection_name'])
                district['all'][ svc['connection_name'] ] = {
                    "name": svc['connection_name'],
                    "ip" : svc['connection_ip'],
                    "port" : svc['connection_port'],
                    "type" : svc['type'],
                    "login" : svc['specific_data']['login'],
                    "password" : svc['specific_data']['password'],
                    "server" : svc['specific_data']['server'],
                }
                district['kaspersky'][ svc['connection_name'] ] = district['all'][ svc['connection_name'] ]

    def __load_dl(self, district_name: str) -> None:
        district = self.__get_district(district_name)
        district['dallas_lock'] = {}
        for svc in self.__services:
            if svc['active'] and svc['type'] == 'dallas_lock':
                self.__check_exist(svc['connection_name'])
                district['all'][ svc['connection_name'] ] = {
                    "name": svc['connection_name'],
                    "ip" : svc['connection_ip'],
                    "port" : svc['connection_port'],
                    "type" : svc['type'],
                    "server": svc['specific_data']['server']
                }
                district['dallas_lock'][ svc['connection_name'] ] = district['all'][ svc['connection_name'] ]

    def __load_database(self, district_name: str) -> None:
        district = self.__get_district(district_name)
        district['database'] = {}
        for svc in self.__services:
            if svc['active'] and svc['type'] == 'database':
                self.__check_exist(svc['connection_name'])
                district['all'][ svc['connection_name'] ] = {
                    "name": svc['connection_name'],
                    "ip" : svc['connection_ip'],
                    "port" : svc['connection_port'],
                    "type" : svc['type'],
                    "database" : svc['specific_data']['database_name'],
                    "driver" : svc['specific_data']['drivername'],
                    "username" : svc['specific_data']['username'],
                    "password" : svc['specific_data']['password']
                }
                district['database'][ svc['connection_name'] ] = district['all'][ svc['connection_name'] ]

    def __check_exist(self, connection_name: str) -> None:
        for district in self.districts_services:
            if connection_name in self.__get_district(district)['all']:
                assert False, "Connecation name (" + connection_name + ") has duplicated."

    def __get_district(self, name):
        if name in self.districts_services:
            return self.districts_services[name]
        else:
            assert False, 'Service has unknown district'

config = Configuration()
services = ServicesConfig(config)

JSON_str = str
