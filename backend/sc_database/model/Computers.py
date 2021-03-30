from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from backend.sc_database.model.Adapters import Adapters
from backend.sc_database.model.BaseModel import BaseModel
from backend.sc_database.model.Logons import Logons


class Computers(BaseModel):
    __tablename__ = 'Computers'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(128), nullable=False, unique=True)
    comment = Column(Text)
    created = Column(DateTime, nullable=False, default=datetime.now())

    addresses = relationship('Adapters', back_populates='computer')
    logons = relationship('Logons', back_populates='computer')

    def __repr__(self):
        return f'<Computers (name: {self.name})>'