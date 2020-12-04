from backend.sc_config.config import ServicesConfig, services as services_config
from backend.sc_services.DistrinctServices import DistinctServices


#TYPES of services
from backend.sc_services.services.ActiveDirectoryService import ActiveDirectoryService
from backend.sc_services.services.DallasLockService import DallasLockService
from backend.sc_services.services.DatabaseService import DatabaseService
from backend.sc_services.services.KasperskyService import KasperskyService

AD = 'active_directory'
DALLAS = 'dallas_lock'
KASPERSKY = 'kaspersky'
DATABASE = 'database'

class ServiceManager:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ServiceManager, cls).__new__(cls)
            cls.instance.__init_services()
        return cls.instance

    def __init_services(self):
        __services = {}
        self.districts_services = {}
        self.__services_config = services_config
        distincts_services = self.__services_config.districts_services
        for distinct_name in distincts_services:
            services_object = self.__add_disctinct(distinct_name)
            for svc_district in distincts_services[distinct_name]['all']:
                svc = distincts_services[distinct_name]['all'][svc_district]
                self.__create_service(distinct_name, svc)

    def __add_disctinct(self, name: str) -> DistinctServices:
        if name not in self.districts_services:
            self.districts_services[name] = DistinctServices(name)
        return self.districts_services[name]

    def __create_service(self, distinct_name: str, configuration: dict) -> None:
        if configuration['type'] == AD:
            isAdded = self.districts_services[distinct_name].add_service(ActiveDirectoryService(configuration))
            if not isAdded:
                assert "Service of " + distinct_name + " district can'tt add service with name - " + configuration['name']
            return
        if configuration['type'] == DALLAS:
            self.districts_services[distinct_name].add_service(DallasLockService(configuration))
            return
        if configuration['type'] == KASPERSKY:
            self.districts_services[distinct_name].add_service(KasperskyService(configuration))
            return
        if configuration['type'] == DATABASE:
            self.districts_services[distinct_name].add_service(DatabaseService(configuration))
            return

    def get_service(self, district, name):
        return self.districts_services[district].all[name]

    def _get_services_of_district(self, district_name):
        assert not district_name in self.districts_services, f'District name not found ({district_name})'
        return self.districts_services[district_name]

    def _get_kaspersky(self, district_name):
        district = self._get_services_of_district(district_name)
        return district['kaspersky']
