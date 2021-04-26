from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from backend.sc_database.model.BaseModel import BaseModel


class Adapters(BaseModel):
    __tablename__ = 'Adapters'

    Addresses_id = Column(Integer, ForeignKey('Addresses.id'), primary_key=True, nullable=False)
    Computers_id = Column(Integer, ForeignKey('Computers.id'), primary_key=True, nullable=False)

    name = Column(String(64))

    updated = Column(DateTime, default=datetime.now())
    created = Column(DateTime, default=datetime.now())

    # computer = relationship('Computers', back_populates='addresses')
    # address = relationship('Addresses', back_populates='computers')

    def __repr__(self):
        return f'<Adapters (Computers_id: {self.Computers_id})>'