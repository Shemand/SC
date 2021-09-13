from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean, select
from sqlalchemy.orm import relationship
from sqlalchemy_utils import create_view

from .AddressesTable import AddressesTable
from .BaseModel import BaseTableModel
from .OperationSystemsTable import OperationSystemsTable


class PuppetsTable(BaseTableModel):
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
class PuppetView(BaseTableModel):
    _create_query = select([
        PuppetsTable.id.label('id'),
        PuppetsTable.Computers_id.label('Computers_id'),
        AddressesTable.ipv4.label('puppet_ip'),
        OperationSystemsTable.name.label('puppet_os'),
        PuppetsTable.board_serial_number.label('board_serial_number'),
        PuppetsTable.astra_update.label('astra_update'),
        PuppetsTable.environment.label('environment'),
        PuppetsTable.domain.label('domain'),
        PuppetsTable.serial_number.label('serial_number'),
        PuppetsTable.isVirtual.label('isVirtual'),
        PuppetsTable.mac.label('mac'),
        PuppetsTable.kesl_version.label('kesl_version'),
        PuppetsTable.klnagent_version.label('klnagent_version'),
        PuppetsTable.uptime_seconds.label('uptime_seconds'),
        PuppetsTable.isDeleted.label('isDeleted'),
        PuppetsTable.updated.label('updated'),
        PuppetsTable.created.label('created')
    ]).select_from(PuppetsTable.__table__.join(AddressesTable, PuppetsTable.Addresses_id == AddressesTable.id, isouter=True)
                   .join(OperationSystemsTable, PuppetsTable.OperationSystems_id == OperationSystemsTable.id, isouter=True))
    __tablename__ = 'puppet_view'
    __table__ = create_view('puppet_view', _create_query, BaseTableModel.metadata)

# At this point running the following yields 0, as expected,
# indicating that the view has been constructed on the server 
# engine.execute(select([func.count('*')], from_obj=MyView)).scalar()
