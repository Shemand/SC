import sqlalchemy

from .StorageRepository import StorageRepository
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine, select
from sqlalchemy.engine.url import URL
from sqlalchemy.dialects.postgresql import insert

# initialize models
from sqlalchemy_utils import create_view

from .db_model import DBmodels
from ..sc_entities.models import Unit


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

    def get_id_ip(self, ip):
        query = insert(self.ip).values(ipv4=ip).on_conflict_do_nothing(index_elements=['ipv4'])
        self.engine.execute(query)
        query = select([self.ip.c.id]).where(self.ip.c.ipv4 == ip)
        id = self.engine.execute(query).fetchone()['id']
        return id

    def get_id_os(self, os_name):

        def _extract_os_type(os_name):
            if os_name.lower().find('win') != -1:
                return False
            return True

        query = insert(self.os).values(name=os_name, isUnix=_extract_os_type(os_name)).on_conflict_do_nothing(index_elements=['name'])
        self.engine.execute(query)
        query = select([self.os.c.id]).where(self.os.c.name == os_name)
        id = self.engine.execute(query).fetchone()['id']
        return id


    def get_unit(self, unit_name):
        query = select([self.units.c.]).where(name=unit_name).limit(1)
        row = self.engine.execute(query).fetchone()
        if row:
            return Unit(name=)
        query = select([self.ip.c.id]).where(self.ip.c.ipv4 == ip)
        id = self.engine.execute(query).fetchone()['id']
        return id
    #
    # def get_computer(self, computer_name):
    #     def _extract_unit(computer_name):
    #         if os_name.lower().find('win') != -1:
    #             return False
    #         return True
    #
    #     query = insert(self.os).values(name=computer_name, unit_id=_extract_os_type(os_name)).on_conflict_do_nothing(
    #         index_elements=['name'])
    #     self.engine.execute(query)
    #     query = select([self.os.c.id]).where(self.os.c.name == os_name)
    #     id = self.engine.execute(query).fetchone()['id']
    #     return id
