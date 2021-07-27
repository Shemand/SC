from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, select
from sqlalchemy.orm import relationship
from sqlalchemy_utils import create_view

from .Addresses import Addresses
from .BaseModel import BaseModel
from .OperationSystems import OperationSystems


class Kaspersky(BaseModel):
    __tablename__ = 'Kaspersky'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Computers_id = Column(Integer, ForeignKey('Computers.id'), nullable=False)
    OperationSystems_id = Column(Integer, ForeignKey('OperationSystems.id'))
    Addresses_id = Column(Integer, ForeignKey('Addresses.id'))
    agent_version = Column(String(32))
    security_version = Column(String(32))
    server = Column(String(32), nullable=False)
    isDeleted = Column(DateTime)
    updated = Column(DateTime, nullable=False, default=datetime.now())
    created = Column(DateTime, nullable=False, default=datetime.now())

    # computer = relationship('Computers', backref='kaspersky')

    def __repr__(self):
        return f'<Kaspersky ({self.computer.name})>'


class KasperskyView(BaseModel):
    _create_query = select([
        Kaspersky.id.label('id'),
        Kaspersky.Computers_id.label('Computers_id'),
        Addresses.ipv4.label('kl_ip'),
        OperationSystems.name.label('kl_os'),
        Kaspersky.agent_version.label('agent_version'),
        Kaspersky.security_version.label('security_version'),
        Kaspersky.server.label('server'),
        Kaspersky.isDeleted.label('isDeleted'),
        Kaspersky.updated.label('updated'),
        Kaspersky.created.label('created')
    ]).select_from(Kaspersky.__table__.join(Addresses, Kaspersky.Addresses_id == Addresses.id, isouter=True)
                   .join(OperationSystems, Kaspersky.OperationSystems_id == OperationSystems.id, isouter=True))
    __tablename__ = 'kasperksy_view'
    __table__ = create_view('kaspersky_view', _create_query, BaseModel.metadata)
