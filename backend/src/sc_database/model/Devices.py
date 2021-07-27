from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime

from .BaseModel import BaseModel


class Devices(BaseModel):
    __tablename__ = 'Devices'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Addresses_id = Column(Integer, ForeignKey('Addresses.id'))
    Units_id = Column(Integer, ForeignKey('Units.id'), nullable=False)
    name = Column(String(128), nullable=False)
    comment = Column(Text)
    updated = Column(DateTime, nullable=False, default=datetime.now())
    created = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'<Devices (name: {self.name})>'