from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine.url import URL

# initialize models
from .model.BaseModel import BaseModel
from .model.Adapters import Adapters
from .model.Computers import Computers
from .model.CryptoGateways import CryptoGateways
from .model.Addresses import Addresses
from .model.Computers_ActiveDirectory import Computers_ActiveDirectory
from .model.DallasLock import DallasLock
from .model.Devices import Devices
from .model.Kaspersky import Kaspersky
from .model.Logons import Logons
from .model.OperationSystems import OperationSystems
from .model.PuppetEvents import PuppetEvents
from .model.Puppets import Puppets
from .model.Units import Units
from .model.Users import Users
from .model.Users_ActiveDirectory import Users_ActiveDirectory

from .actions.AddressActions import AddressActions
from .actions.ComputerActions import ComputerActions

class DatabaseClass(object):

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

    def __init__(self, database_config) -> None:
        db_url = {
            'database': database_config['database'],
            'drivername': database_config['driver'],
            'username': database_config['username'],
            'password': database_config['password'],
            'host': database_config['ip'],
            'query': {'charset': 'utf8'}
        }
        self.__engine = create_engine(URL(**db_url), echo=False, encoding="utf8", pool_size=10)
        self.__metadata = BaseModel.metadata.create_all(self.engine)
        self.__session = Session(bind=self.engine)
        self.session.commit()
        self.Addresses = AddressActions(self, DatabaseClass.Addresses)
        self.Computers = ComputerActions(self, DatabaseClass.Addresses)

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def metadata(self) -> MetaData:
        return self.__metadata

    @property
    def session(self) -> Session:
        return self.__session

    def commit(self):
        return self.session.commit()

    def query(self, query_cls):
        return self.session.query(query_cls)

    def add(self, query_obj):
        return self.session.add(query_obj)

    def get(self, db_model, name=None, id=None):
        assert not (name and id), 'Arguments of get must have only one argument for search id or name'
        params = self.__tune_params(id, name)
        instance = self.session.query(db_model.TABLE).filer_by(**params).first()
        return instance

    def get_or_create(self, db_model, name):
        instance = None
        params = {db_model.MAIN_COLUMN:name}
        if name:
            instance = self.session.query(db_model.TABLE).filter_by(**params).first()
        if instance:
            return instance
        return self.__create_minimal_obj(self, **params)

    def __create_minimal_obj(self, db_model, **kwargs):
        instance = db_model.TABLE(**kwargs)
        self.add(instance)
        self.commit()
        return instance

    def exists(self, db_model, id: int = None, name: str = None) -> bool:
        params = db_model.__tune_params(id, name)
        instance = self.query(db_model.TABLE).filer_by(**params).first()
        if instance:
            return True
        return False

    def __tune_params(self, db_model, id: int = None, name: str = None):
        params = {
            db_model.MAIN_COLUMN : name,
            db_model.ID_COLUMN : id
        }
        params = {key : params[key] for key in params if params[key] is not None}
        return params
