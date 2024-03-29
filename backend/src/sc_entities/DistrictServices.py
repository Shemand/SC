from ..sc_repositories.ActiveDirectoryRepository import ActiveDirectoryRepository
from ..sc_repositories.DallasLockRepository import DallasLockRepository
from ..sc_repositories.KasperskyRepository import KasperskyRepository
from ..sc_repositories.PuppetRepository import PuppetRepository


class DistrictServices():
    def __init__(self, district):
        self.all = {}
        self.kaspersky = []
        self.ad = []
        self.dallas = []
        self.puppet = []
        self.services_status = {}
        self.district = district

    def add_service(self, service):
        if isinstance(service, ActiveDirectoryRepository):
            self.ad.append(service)
        elif isinstance(service, KasperskyRepository):
            self.kaspersky.append(service)
        elif isinstance(service, DallasLockRepository):
            self.dallas.append(service)
        elif isinstance(service, PuppetRepository):
            self.puppet.append(service)
        else:
            raise RuntimeError('Unknown type of service')
        self.all[service.name] = service

    def get_service(self, service_name):
        return self.all[service_name]

    def get_active_directory_services(self):
        return self.ad

    def get_dallas_lock_services(self):
        return self.dallas

    def get_kaspersky_services(self):
        return self.kaspersky

    def get_puppet_services(self):
        return self.puppet

    def authenticate_user(self, login, base64_password):
        for service in self.get_active_directory_services():
            if service.authenticate_user(login, base64_password):
                return True
        return False

    def __dict__(self, service_name):
        return self.get_service(service_name)