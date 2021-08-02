from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .BaseModel import BaseModel


class Logons(BaseModel):
    __tablename__ = 'Logons'

    Computers_id = Column(Integer, ForeignKey('Computers.id'), primary_key=True, nullable=False)
    Users_id = Column(Integer, ForeignKey('Users.id'), primary_key=True, nullable=False)
    OperationSystems_id = Column(Integer, ForeignKey('OperationSystems.id'))
    created = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'<Logons ({self.computer.name} - {self.user.username})>'