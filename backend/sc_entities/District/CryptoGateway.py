import ipaddress


class CryptoGateway:

    def __init__(self, district, name, information):
        self._district = district
        self._name = name
        self._caption = information['caption']
        self._address = information['address']
        self._mask = int(information['mask'])
        self._unit = information['unit']
        self._network = self.__build_network()

    @property
    def district(self):
        return self._name

    @property
    def name(self):
        return self._name

    @property
    def caption(self):
        return self._caption

    @property
    def address(self):
        return self._address

    @property
    def mask(self):
        return self._mask

    @property
    def unit(self):
        return self._unit

    @property
    def network(self):
        return self._network

    def __build_network(self):
        return ipaddress.ip_network(f'{self.address}/{str(self.mask)}')

    def byUnit(self, unit_name: str) -> bool:
        if unit_name == self.unit:
            return True
        return False