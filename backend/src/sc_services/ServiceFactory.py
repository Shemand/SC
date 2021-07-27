from .ActiveDirectoryService import ActiveDirectoryService
from .DallasLockService import DallasLockService
from .KasperskyService import KasperskyService
from .PuppetServices import PuppetService

_services_relations = {
    'active_directory' : ActiveDirectoryService,
    'kaspersky' : KasperskyService,
    'dallas_lock' : DallasLockService,
    'puppet' : PuppetService
}

class ServiceFactory:
    @staticmethod
    def create_service(district, service_config):
        specific_data = service_config['specific_data']
        del service_config['specific_data']
        main_config = service_config
        service_type = main_config['type']
        if not service_type in _services_relations:
            raise RuntimeError(f'ServiceFactory.create_service unknown type of service "{main_config["connection_name"]}"')
        return _services_relations[service_type](district, main_config, specific_data)
