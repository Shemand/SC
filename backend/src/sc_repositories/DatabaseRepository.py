from typing import Optional

import sqlalchemy

from .StorageRepository import StorageRepository
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine, select, insert
from sqlalchemy.engine.url import URL

# initialize models
from sqlalchemy_utils import create_view

from .db_model import DBmodels
from ..sc_entities.models import Unit, Computer, Ip, Os


class DatabaseRepository(StorageRepository):
    __metadata: MetaData
    __engine: Engine
    __session: Session
    isUpdating = False

    def __init__(self, database_config) -> None:
        db_url = {
            'database': database_config['database'],
            'drivername': database_config['driver'],
            'username': database_config['username'],
            'password': database_config['password'],
            'host': database_config['ip']
        }
        self.__engine = create_engine(URL.create(**db_url), echo=False, encoding="utf8", pool_size=10)
        BaseModel = declarative_base()
        self.__metadata = BaseModel.metadata
        self._models = DBmodels(self.__metadata)
        self.users = self._models.users
        self.ad_users = self._models.active_directory_users
        self.kaspersky = self._models.kaspersky
        self.os = self._models.os
        self.puppet_events = self._models.puppet_events
        self.puppets = self._models.puppets
        self.units = self._models.units
        self.logons = self._models.logons
        self.cg = self._models.crypto_gateways
        self.computers = self._models.computers
        self.ad_computers = self._models.active_directory_computers
        self.ip = self._models.ip
        self.dallas = self._models.dallas
        self.adapters = self._models.adapters
        self.__metadata.create_all(self.engine)
        # self.engine.execute("")

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def metadata(self) -> MetaData:
        return self.__metadata

    def get_ip(self, ip):
        query = select([self.ip]).where(self.ip.c.ipv4 == ip).limit(1)
        row = self.engine.execute(query).fetchone()
        if row:
            return Ip(id_=row['id'], ipv4=row['ipv4'], isAllowed=row['isAllowed'])
        query = insert(self.ip).values(ipv4=ip)
        self.engine.execute(query)
        query = select([self.ip]).where(self.ip.c.ipv4 == ip)
        row = self.engine.execute(query).fetchone()
        return Ip(id_=row['id'], ipv4=row['ipv4'], isAllowed=row['isAllowed'])

    def get_os(self, os_name):

        def _extract_os_type(os_name):
            if os_name.lower().find('win') != -1:
                return False
            return True

        query = select([self.os]).where(self.os.c.name == os_name).limit(1)
        row = self.engine.execute(query).fetchone()
        if row:
            return Os(id_=row['id'], name=row['name'], isUnix=row['isUnix'])
        query = insert(self.os).values(name=os_name, isUnix=_extract_os_type(os_name))
        self.engine.execute(query)
        query = select([self.os]).where(self.os.c.name == os_name).limit(1)
        row = self.engine.execute(query).fetchone()
        return Os(id_=row['id'], name=row['name'], isUnix=row['isUnix'])

    def get_unit(self, unit_name) -> Optional[Unit]:
        query = select([self.units.c.id, self.units.c.name]).where(self.units.c.name == unit_name).limit(1)
        row = self.engine.execute(query).fetchone()
        if not row:
            return None
        return Unit(id_=row['id'], name=row['name'])

    def get_default_unit(self) -> Unit:
        query = select([self.units.c.id, self.units.c.name]).where(
            self.units.c.name == 'UNKNOWN')  # todo replace default unit from string to config execution
        row = self.engine.execute(query).fetchone()
        return Unit(id_=row['id'], name=row['name'])

    def get_computer(self, computer_name):

        def _extract_unit(db, computer_name):
            prefix_end_index = computer_name.find('-')
            if prefix_end_index == -1:
                return db.get_default_unit()
            computer_prefix = computer_name[:computer_name.find('-')]
            unit = db.get_unit(computer_prefix)
            if not unit:
                return db.get_default_unit()
            return unit

        computer_name = computer_name.upper()
        unit = _extract_unit(self, computer_name)
        query = select([self.computers.c.id, self.computers.c.name]).where(self.computers.c.name == computer_name)
        row = self.engine.execute(query).fetchone()
        if row:
            return Computer(id_=row['id'], name=computer_name, unit=unit)
        query = insert(self.computers).values(name=computer_name, unit_id=select([self.units.c.id]).where(self.units.c.name == unit.name))
        self.engine.execute(query)
        query = select([self.computers.c.id, self.computers.c.name]).where(self.computers.c.name == computer_name).limit(1)
        row = self.engine.execute(query)
        return Computer(id_=row['id'], name=row['name'], unit=unit)

