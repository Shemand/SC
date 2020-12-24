from backend.sc_entities.District.DistrictServices import DistrictServices

class ServiceManager:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ServiceManager, cls).__new__(cls)
            cls.instance.__init_services()
        return cls.instance

    def __init_services(self):
        __services = {}
        self.districts = None