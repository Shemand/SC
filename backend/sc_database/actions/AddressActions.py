from backend.sc_database.model.Addresses import Addresses
from .DatabaseActionsAbstract import DatabaseActionsAbstract


class AddressActions(DatabaseActionsAbstract):

    def __init__(self, database, model):
        super().__init__(database, model)

