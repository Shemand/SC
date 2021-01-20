
class DatabaseActionsAbstract:

    def __init__(self, database, model):
        self.database = database
        self.model = model
        self.requires = {}
        self.primary = {}
        self.unique = {}
        self._initialize_columns_settings()

    def get(self, database, **params):
        params = self._filter_unique(**params)
        if params:
            instance = database.query(self.model).filter_by(**params).first()
            if instance:
                return instance
        return None

    def get_or_create(self, database, **params):
        unique = self._filter_unique(**params)
        instance = self.get(database, **unique)
        if instance:
            return instance
        instance = self.create_minimal_obj(database, **params)
        return instance

    def exists(self, database, **params) -> bool:
        instance = self.get(database, **params)
        if instance:
            return True
        return False

    def create_minimal_obj(self, database, **params):
        if self._requires_exists(**params):
            instance = self.model(**params)
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

    def _filter_unique(self, **params):
        if self._least_one_unique(**params):
            to_return = {}
            for key in params:
                if key in self.unique:
                    to_return[key] = params[key]
            return to_return
        raise Exception('_filter_unique: no one unique columns no exist')

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

    def _least_one_unique(self, **params):
        for key in self.unique:
            if key in params:
                return True
        return False

    def _requires_exists(self, **params):
        for key in self.requires:
            if key not in params:
                return False
        return True

    def _initialize_columns_settings(self):
        self.requires = {}
        self.primary = {}
        self.unique = {}
        columns = self.model.__table__.c
        for col in columns:
            if not col.nullable\
                and not col.default\
                and not col.autoincrement:
                self.requires[col.key] = col
            if col.primary_key:
                self.primary[col.key] = col
            if col.unique or col.primary_key:
                self.unique[col.key] = col