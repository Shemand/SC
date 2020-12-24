from backend.sc_services.services.ServiceAbstract import ServiceAbstract
from backend.sc_services.services.ActiveDirectoryService import ActiveDirectoryService
from backend.sc_services.services.DallasLockService import DallasLockService
from backend.sc_services.services.KasperskyService import KasperskyService


class DistrictServices:
    AD = 'active_directory'
    DALLAS = 'dallas_lock'
    KASPERSKY = 'kaspersky'

    TYPES = [AD, DALLAS, KASPERSKY]

    def __init__(self, name):
        self.name: str = name
        self.all: dict = {}
        self.ad: dict = {}
        self.kaspersky: dict = {}
        self.dallas_lock: dict = {}
        self.database: dict = {}

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
        return False

    def get_service(self, service_name: str) -> ServiceAbstract:
        if service_name in self.all:
            return self.all[service_name]
        assert 'You attempt get service with unknown name.'
        # return None
