from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .BaseModel import BaseModel


class AdaptersTable(BaseModel):
    __tablename__ = 'Adapters'

    Addresses_id = Column(Integer, ForeignKey('Addresses.id'), primary_key=True, nullable=False)
    Computers_id = Column(Integer, ForeignKey('Computers.id'), primary_key=True, nullable=False)

    name = Column(String(64))

    updated = Column(DateTime, default=datetime.now())
    created = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f'<Adapters (Computers_id: {self.Computers_id})>'