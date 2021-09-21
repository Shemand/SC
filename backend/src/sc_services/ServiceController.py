from backend.src.sc_repositories.DatabaseRepository import DatabaseRepository


class ServiceController:
    def __new__(cls, *args, **kwargs):
        if 'instance' in cls:
            cls.instance = super(ServiceController, cls).__new__(cls)
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

