from backend.sc_entities.District.DistrictServices import DistrictServices

from multiprocessing import Process
from time import sleep


class ServiceManager(Process):

    def __new__(cls, districts):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ServiceManager, cls).__new__(cls)
            cls.__created = True
        return cls.instance

    def __init__(self, districts):
        if ServiceManager.__created:
            Process.__init__(self)
            self.daemon = True
            ServiceManager.__created = False
            self.districts_services = {}
            self.all = {}
            self.services_status = {}
            for district in self.districts:
                if not district.name in self.districts_services:
                    self.districts_services[district.name] = {}
                services = district.services
                ds = self.districts_services[district.name]
                for service in services.all:
                    ds[service.name] = service

    def show_status(self, district, service_name=None):
        if service_name:
            return self.districts_services[district][service_name].status
        return { service_name : self.districts_services[district][service_name].status
                 for service_name in self.districts_services[district]}


    def run(self):
        while True:
            pass

