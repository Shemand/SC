from .StorageRepository import StorageRepository
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine.url import URL

# initialize models
from sqlalchemy_utils import create_view


from .DatabaseModels.BaseModel import BaseModel
from .DatabaseModels.Adapters import Adapters
from .DatabaseModels.Computers import Computers
from .DatabaseModels.CryptoGateways import CryptoGateways
from .DatabaseModels.Addresses import Addresses
from .DatabaseModels.Computers_ActiveDirectory import Computers_ActiveDirectory
from .DatabaseModels.DallasLock import DallasLock
from .DatabaseModels.Devices import Devices
from .DatabaseModels.Kaspersky import Kaspersky
from .DatabaseModels.Logons import Logons
from .DatabaseModels.OperationSystems import OperationSystems
from .DatabaseModels.PuppetEvents import PuppetEvents
from .DatabaseModels.Puppets import Puppets, PuppetView
from .DatabaseModels.Units import Units
from .DatabaseModels.Users import Users
from .DatabaseModels.Users_ActiveDirectory import Users_ActiveDirectory


class DatabaseRepository(StorageRepository):
    __metadata: MetaData
    __engine: Engine
    __session: Session
    isUpdating = False

    Adapters = Adapters
    Users = Users
    Computers = Computers
    CryptoGateways = CryptoGateways
    Addresses = Addresses
    Computers_ActiveDirectory = Computers_ActiveDirectory
    DallasLock = DallasLock
    Devices = Devices
    Kaspersky = Kaspersky
    Logons = Logons
    OperationSystems = OperationSystems
    PuppetEvents = PuppetEvents
    Puppets = Puppets
    Units = Units
    Users = Users
    Users_ActiveDirectory = Users_ActiveDirectory
    PuppetView = PuppetView


    def __init__(self, district, database_config) -> None:
        self.district = district
        db_url = {
            'database': database_config['database'],
            'drivername': database_config['driver'],
            'username': database_config['username'],
            'password': database_config['password'],
            'host': database_config['ip']
        }
        self.__engine = create_engine(URL.create(**db_url), echo=False, encoding="utf8", pool_size=10)
        self.__metadata = BaseModel.metadata.create_all(self.engine)
        self.__session = Session(bind=self.engine)
        self.session.commit()


    @property
    def engine(self) -> Engine:
        return self.__engine


    @property
    def metadata(self) -> MetaData:
        return self.__metadata


    @property
    def session(self) -> Session:
        return self.__session


    def get_local_session(self):
        return Session(bind=self.engine)


    def commit(self):
        return self.session.commit()


    def query(self, query_cls):
        return self.session.query(query_cls)


    def add(self, query_obj):
        return self.session.add(query_obj)
