from backend.sc_entities.District.CryptoGateway import CryptoGateway


class DistrictUnit:

    def __init__(self, district, name, information):
        self.crypto_gateways = {}
        self.district = district
        self.name = name
        self.caption = information['caption']
        self.dallas_containers = information['dallas_containers']
        self.active_directory_containers = information['active_directory_containers']
        self._kaspersky_services_name = information['kaspersky_services']
        self.services = self.__initialize_services()

    def __initialize_services(self):
        services = {}
        for service_name in self._kaspersky_services_name:
            all_services = self.district._services.all
            if service_name in all_services:
                services[service_name] = all_services[service_name]
                print(f'Service ({service_name}) was connected to {self.district.name} district')
            else:
                print(f'Service ({service_name}) not found in {self.district.name}/services.json')
        return services

    def append_crypto_gateway(self, crypto_gateway: CryptoGateway):
        cg_name = crypto_gateway.name
        assert not cg_name in self.crypto_gateways, f'District Unit already have crypto gateway with name{cg_name}'
        self.crypto_gateways[cg_name] = crypto_gateway

    def __repr__(self):
        return f'<DistrictUnit (name: {self.name})>'