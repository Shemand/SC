import os

from backend.src.sc_repositories.DatabaseRepository import DatabaseRepository


class RepositoryController:
    def __new__(cls, *args, **kwargs):
        if 'instance' in cls:
            cls.instance = super(RepositoryController, cls).__new__(cls)
            cls.instance.__initialization(*args, **kwargs)
        return cls.instance

    def __initialization(self):
        config = {
            "ip": "localhost",
            "port": 5432,
            "database": "sc",
            "driver": "postgresql+psycopg2",
            "username": "shemand",
            "password": "qwerty"
        }
        self.db = DatabaseRepository(config)
        ...

    @property
    def database(self): # todo creating database
        return self.db


class RepositoryFactory:
    ...


class RepositoryStorage:
    ...


class RepositoryConfigs:
    def __init__(self):
        pass

    def __load_json(self):
        pass

    def __load_file(self):
        path = os.getcwd()
        path = os.path.join(path, 'configs')
        path = os.path.join(path, 'new_configs')
        file_path = os.path.join(path, 'repositories')
        file = open()