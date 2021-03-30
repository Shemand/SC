from backend.sc_services.services.ServiceAbstract import ServiceAbstract
from backend.sc_services.services.ActiveDirectoryService import ActiveDirectoryService
from backend.sc_services.services.DallasLockService import DallasLockService
from backend.sc_services.services.KasperskyService import KasperskyService


class DistrictServices:
    AD = 'active_directory'
    DALLAS = 'dallas_lock'
    KASPERSKY = 'kaspersky'

    TYPES = {
        AD : ActiveDirectoryService,
        DALLAS : DallasLockService,
        KASPERSKY : KasperskyService
    }

    def __init__(self, name):
        self._name: str = name
        self._all: dict = {}
        self._ad: dict = {}
        self._kaspersky: dict = {}
        self._dallas_lock: dict = {}
        self._database: dict = {}

    @property
    def name(self):
        return self._name

    @property
    def all(self):
        return self._all

    @property
    def ad(self):
        return self._ad

    @property
    def kaspersky(self):
        return self._kaspersky

    @property
    def dallas_lock(self):
        return self._dallas_lock

    @property
    def database(self):
        return self._database

    def __get_service_instance(self, type: str, settings) -> ServiceAbstract:
        assert type in DistrictServices.TYPES, f'Unknown DistinctServices.TYPE in service with name: "{settings["name"]}"'
        return DistrictServices.TYPES[type](settings)

    def add_service(self, object_type, settings) -> bool:
        service_object = self.__get_service_instance(object_type, settings)
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
