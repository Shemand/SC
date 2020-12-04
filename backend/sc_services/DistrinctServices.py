from backend.sc_services.ServiceAbstract import ServiceAbstract
from backend.sc_services.services.ActiveDirectoryService import ActiveDirectoryService
from backend.sc_services.services.DallasLockService import DallasLockService
from backend.sc_services.services.DatabaseService import DatabaseService
from backend.sc_services.services.KasperskyService import KasperskyService


class DistinctServices:

    name: str
    ad: dict
    kaspersky: dict
    dallas_lock: dict
    database: dict

    def __init__(self, name):
        self.name = name
        self.all = {}
        self.ad = {}
        self.kaspersky = {}
        self.dallas_lock = {}
        self.database = {}

    def add_service(self, service_object: ServiceAbstract) -> bool:
        if service_object.name in self.all:
            assert 'Connection name(' + service_object.name + ') of service has duplicated. Edit configuration file.'
            return False
        if isinstance(service_object, ActiveDirectoryService):
                self.ad[service_object.name] = service_object
                self.all[service_object.name] = self.ad[service_object.name]
                return True
        if isinstance(service_object, KasperskyService):
                self.kaspersky[service_object.name] = service_object
                self.all[service_object.name] = self.kaspersky[service_object.name]
                return True
        if isinstance(service_object, DallasLockService):
                self.dallas_lock[service_object.name] = service_object
                self.all[service_object.name] = self.dallas_lock[service_object.name]
                return True
        if isinstance(service_object, DatabaseService):
                self.database[service_object.name] = service_object
                self.all[service_object.name] = self.database[service_object.name]
                return True
        return False

    def get_service(self, service_name: str) -> ServiceAbstract:
        if service_name in self.all:
            return self.all[service_name]
        assert 'You attempt get service with unknown name.'
        # return None
