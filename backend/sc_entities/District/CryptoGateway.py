import ipaddress


class CryptoGateway:

    def __init__(self, district, name, information):
        self.district = district
        self.name = name
        self.caption = information['caption']
        self.address = information['address']
        self.mask = int(information['mask'])
        self.unit = information['unit']
        self.network = self.__build_network()

    def __build_network(self):
        return ipaddress.ip_network(f'{self.address}/{str(self.mask)}')

    def byUnit(self, unit_name: str) -> bool:
        if unit_name == self.unit:
            return True
        return False