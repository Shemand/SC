from sqlalchemy import select, insert, update, delete

from .ServicesInterfaces import ServiceAbstract
from ..sc_config.config import config
from ..sc_entities.models import Ip
from ..sc_repositories.DatabaseModels.AddressesTable import AddressesTable
from ..sc_repositories.DatabaseModels.CryptoGatewaysTable import CryptoGatewaysTable


class IpService(ServiceAbstract):

    @staticmethod
    def _return_model_fields(row):
        return {
            "ipv4": row['ipv4'],
            "isAllowed": row['isAllowed'],
        }

    def all(self):
        fields = [AddressesTable.ipv4, AddressesTable.isAllowed]
        query = select(fields)
        rows = self.db.engine.execute(query).fetchall()
        addresses = [Ip(**type(self)._return_model_fields(row)) for row in rows]
        return addresses

    def get(self, ip: str):
        fields = [AddressesTable.ipv4, AddressesTable.isAllowed]
        query = select(fields).where(AddressesTable.ipv4 == ip).limit(1)
        row = self.db.engine.execute(query).fetchone()
        if not row:
            return None
        ip = Ip(**type(self)._return_model_fields(row))
        return ip

    def create(self, model: Ip):
        params = {
            "ipv4": model.ipv4,
            "isAllowed": model.isAllowed,
        }
        query = insert(AddressesTable).values(**params)
        self.db.engine.execute(query)
        return True

    def update(self, model: Ip):
        db_model = self.get(model.ipv4)
        if model == db_model:
            return False
        values = {
            "ipv4": model.ipv4,
            "isAllowed": model.isAllowed,
        }
        if 'crypto_gateways' in model.__fields__:
            values['CryptoGateways_id'] = select([CryptoGatewaysTable.id]).where(CryptoGatewaysTable.name == model.crypto_gateway.name).limit(1)
        query = update(AddressesTable).values(**values).where(AddressesTable.ipv4 == model.ipv4)
        self.db.engine.execute(query)
        return True

    def delete(self, ip):
        query = delete(AddressesTable).where(AddressesTable.ipv4 == ip)
        self.db.engine.execute(query)

    def get_or_create(self, ip: str):
        ip = self.get(ip)
        if ip:
            return ip
        model = Ip(ipv4=ip, isAllowed=True)
        return self.create(model)

    def is_exists(self, ip):
        ip = self.get(ip)
        if ip:
            return True
        return False