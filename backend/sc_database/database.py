from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from backend.config import config, services
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine.url import URL


class Database(object):

    __metadata: MetaData
    __engine: Engine
    __session: Session
    isUpdating = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
            cls.instance.init()
        return cls.instance

    def init(self) -> None:
        self.__metadata = MetaData()
        db_url = {
            'database': services['SZO']['mysql_database']['database'],
            'drivername': services['SZO']['mysql_database']['driver'],
            'username': services['SZO']['mysql_database']['username'],
            'password': services['SZO']['mysql_database']['password'],
            'host': services['SZO']['mysql_database']['ip'],
            'query': {'charset': 'utf8'}
        }
        self.__engine = create_engine(URL(**db_url), echo=False, encoding="utf8", pool_size=10)
        self.__session = Session(bind=self.engine)

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def session(self) -> Session:
        return self.__session
