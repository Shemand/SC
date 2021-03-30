from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from backend.sc_database.model.BaseModel import BaseModel


class Kaspersky(BaseModel):
    __tablename__ = 'Kaspersky'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Computers_id = Column(Integer, ForeignKey('Computers.id'), nullable=False)
    OperationSystems_id = Column(Integer, ForeignKey('OperationSystems.id'))
    Addresses_id = Column(Integer, ForeignKey('Addresses.id'))
    agent_version = Column(String(32))
    security_version = Column(String(32))
    server = Column(String(32), nullable=False)
    updated = Column(DateTime, nullable=False, default=datetime.now())
    created = Column(DateTime, nullable=False, default=datetime.now())

    computer = relationship('Computers', backref='kaspersky')

    def __repr__(self):
        return f'<Kaspersky ({self.computer.name})>'