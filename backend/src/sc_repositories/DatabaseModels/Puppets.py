from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean, select
from sqlalchemy.orm import relationship
from sqlalchemy_utils import create_view

from .Addresses import Addresses
from .BaseModel import BaseModel
from .OperationSystems import OperationSystems


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

    def __repr__(self):
        return f'<Puppets ({self.computer.name})>'

# attaches the view to the metadata using the select statement


# provides an ORM interface to the view
class PuppetView(BaseModel):
    _create_query = select([
        Puppets.id.label('id'),
        Puppets.Computers_id.label('Computers_id'),
        Addresses.ipv4.label('puppet_ip'),
        OperationSystems.name.label('puppet_os'),
        Puppets.board_serial_number.label('board_serial_number'),
        Puppets.astra_update.label('astra_update'),
        Puppets.environment.label('environment'),
        Puppets.domain.label('domain'),
        Puppets.serial_number.label('serial_number'),
        Puppets.isVirtual.label('isVirtual'),
        Puppets.mac.label('mac'),
        Puppets.kesl_version.label('kesl_version'),
        Puppets.klnagent_version.label('klnagent_version'),
        Puppets.uptime_seconds.label('uptime_seconds'),
        Puppets.isDeleted.label('isDeleted'),
        Puppets.updated.label('updated'),
        Puppets.created.label('created')
    ]).select_from(Puppets.__table__.join(Addresses, Puppets.Addresses_id == Addresses.id, isouter=True)
                          .join(OperationSystems, Puppets.OperationSystems_id == OperationSystems.id, isouter=True))
    __tablename__ = 'puppet_view'
    __table__ = create_view('puppet_view', _create_query, BaseModel.metadata)

# At this point running the following yields 0, as expected,
# indicating that the view has been constructed on the server 
# engine.execute(select([func.count('*')], from_obj=MyView)).scalar()
