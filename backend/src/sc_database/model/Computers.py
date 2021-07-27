from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from .Adapters import Adapters
from .BaseModel import BaseModel
from .Logons import Logons


class Computers(BaseModel):
    __tablename__ = 'Computers'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(128), nullable=False, unique=True, index=True)
    comment = Column(Text)
    created = Column(DateTime, nullable=False, default=datetime.now())
    Units_id = Column(Integer, ForeignKey('Units.id'), nullable=False)

    # addresses = relationship('Adapters', back_populates='computer')
    # logons = relationship('Logons', back_populates='computer')

    def __repr__(self):
        return f'<Computers (name: {self.name})>'
