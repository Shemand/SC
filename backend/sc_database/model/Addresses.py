from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from backend.sc_database.model.BaseModel import BaseModel


class Addresses(BaseModel):
    __tablename__ = 'Addresses'

    id = Column(String(16), primary_key=True, nullable=False, autoincrement=True)
    CryptoGateways_id = Column(Integer, ForeignKey('CryptoGateways.id'))
    ipv4 = Column(String(16), nullable=False)
    isAllowed = Column(DateTime)

    computers = relationship('Adapters', back_populates='address')

    def __repr__(self):
        return f'<Addresses (ip: {self.ipv4})>'