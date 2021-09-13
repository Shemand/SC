from backend.src.sc_repositories.StorageRepository import StorageRepository


class CryptoGatewaysRepository(StorageRepository):
    def __init__(self):
        self.load_repository()

    def _load_repository(self):
        file = open('crypto_gateway')

    def create(self):
        pass

    def get(self):
        ...

    def is_include(self, ip):
        ...

   def remove(self, name)