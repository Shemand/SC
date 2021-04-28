from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship

from backend.sc_database.model.BaseModel import BaseModel


class Puppets(BaseModel):
    __tablename__ = 'Puppets'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Computers_id = Column(Integer, ForeignKey('Computers.id'), nullable=False)
    Addresses_id = Column(Integer, ForeignKey('Addresses.id'))
    OperationSystems_id = Column(Integer, ForeignKey('OperationSystems.id'))
    board_serial_number = Column(String(128))
    astra_update = Column(String(32))
    environment = Column(String(64), nullable=False)
    domain = Column(String(64))
    serial_number = Column(String(128))
    isVirtual = Column(Boolean, nullable=False, default=False)
    mac = Column(String(18))
    kesl_version = Column(String(32))
    klnagent_version = Column(String(32))
    uptime_seconds = Column(Integer)
    isDeleted = Column(DateTime)
    updated = Column(DateTime, nullable=False, default=datetime.now())
    created = Column(DateTime, nullable=False, default=datetime.now())

    # computer = relationship('Computers', backref='puppet')

    def __repr__(self):
        return f'<Puppets ({self.computer.name})>'