from backend.sc_database.database import DatabaseClass
from backend.sc_database.model.BaseModel import BaseModel

class DatabaseActionsAbstract:

    def __init__(self, database, model):
        self.database = database
        self.model = model
        self.requires = {}
        self.primary = {}
        self._initialize_primary_and_requires()

    def get(self, database: DatabaseClass, **params):
        params = self._filter_primary(**params)
        if params:
            instance = database.query(self).filter_by(**params).first()
            if instance:
                return instance
        return None

    def get_or_create(self, database: DatabaseClass, **params):
        primary = self._filter_primary(**params)
        instance = self.get(database, **primary)
        if instance:
            return instance
        instance = self.create_minimal_obj(database, **params)
        return instance

    def exists(self, database: DatabaseClass, params) -> bool:
        instance = self.get(database, params)
        if instance:
            return True
        return False

    def create_minimal_obj(self, database: DatabaseClass, **params):
        if self._requires_exists(**params):
            instance = self.table(**params)
            database.add(instance)
            database.commit()
            return instance
        assert False, 'not all columns of requires was gave in params of create_minimal_obj'

    def _filter_primary(self, **params):
        if self._primary_exists(**params):
            to_return = {}
            for key in params:
                if key in self.primary:
                    to_return[key] = params[key]
            return to_return
        raise Exception('_filter_primary: not all primary keys exist')

    def _filter_require(self, **params):
        if self._requires_exists(**params):
            to_return = {}
            for key in params:
                if key in self.requires:
                    to_return[key] = params[key]
            return to_return
        raise Exception('_filter_require: not all requires exist')

    def _primary_exists(self, **params):
        for key in self.primary:
            if key not in params:
                return False
        return True

    def _requires_exists(self, **params):
        for key in self.requires:
            if key not in params:
                return False
        return True

    def _initialize_primary_and_requires(self):
        self.requires = {}
        self.primary = {}
        columns = self.table.__table__.c
        for col in columns:
            if not col.nullable\
                and not col.default\
                and not col.autoincrement:
                self.requires[col.key] = col
            if col.primary_key:
                self.primary[col.key] = col