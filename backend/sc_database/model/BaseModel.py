from sqlalchemy.ext.declarative import declarative_base

BasicModel = declarative_base()

class BaseModel(BasicModel):

    PRIMARY_COLUMNS = []
    REQUIRE_COLUMNS = []

    def __init__(self, *args):
        super().__init__(*args)
        self.__check_configuration()

    def __check_configuration(self):
        assert BaseModel.PRIMARY_COLUMNS is not [], f'Undefined PRIMARY_COLUMNS ({BaseModel.PRIMARY_COLUMNS})'
        assert BaseModel.REQUIRE_COLUMNS is not [], f'Undefined requires keys ({BaseModel.REQUIRE_COLUMNS})'

    def only_requires(self, params):
        to_return = {}
        for key in params:
            if key in BaseModel.PRIMARY_COLUMNS:
                to_return[key] = params[key]


    def __repr__(self):
        return f'BaseModel <qPC({len(self.PRIMARY_COLUMNS)}), qRC({len(self.REQUIRE_COLUNS)})>'