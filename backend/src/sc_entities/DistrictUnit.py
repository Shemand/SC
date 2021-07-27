from .CryptoGateway import CryptoGateway


class DistrictUnit:

    def __init__(self, district, name, information):
        self._raw_information = information
        self._crypto_gateways = {}
        self._district = district
        self._name = name
        self._caption = information['caption']
        self._dallas_containers = information['dallas_containers']
        self._active_directory_containers = information['active_directory_containers']
        self._services_name = information['services']
        self._services = self.__initialize_services()

    @property
    def district(self):
        return self._district

    @property
    def services(self):
        return self._services

    @property
    def name(self):
        return self._name

    @property
    def dl_containers(self):
        return self._dallas_containers

    @property
    def ad_containers(self):
        return self._active_directory_containers

    @property
    def caption(self):
        return self._caption

    @property
    def crypto_gateways(self):
        return self._crypto_gateways

    @property
    def information(self):
        return self._raw_information

    def __initialize_services(self):
        services = {}
        for service_name in self._services_name:
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