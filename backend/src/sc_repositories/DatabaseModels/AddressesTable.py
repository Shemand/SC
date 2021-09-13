from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .BaseModel import BaseModel


class AddressesTable(BaseModel):
    __tablename__ = 'Addresses'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    CryptoGateways_id = Column(Integer, ForeignKey('CryptoGateways.id'))
    ipv4 = Column(String(16), nullable=False, unique=True, index=True)
    isAllowed = Column(DateTime)

    def __repr__(self):
        return f'<Addresses (ip: {self.ipv4})>'